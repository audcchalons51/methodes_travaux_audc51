#!/usr/bin/env python3
"""
Génère la page interactive de l'ETL à partir d'un modèle QGIS (.model3).

Usage :
    python generer_etl.py mon_modele.model3 etl_interactif.html

Le script relit le modèle (traitements, liens, paramètres, positions) et remplace le bloc
<script id="etl-data"> du fichier HTML. Les textes explicatifs (titres, descriptions) sont
dans le dictionnaire META ci-dessous : modifiez-les à votre guise.
"""
import json, re, sys
import xml.etree.ElementTree as ET

# ------------------------------------------------------------------ textes éditables
INPUTS = {
    'nuds_de_cheminement': dict(title='Nœuds de cheminement', mono='noeud_cheminement', desc='geo_standards · points, id_netex', color='blue', x=0, y=80,
        text="Table des nœuds (points) du réseau piéton. Chaque nœud porte un identifiant métier, id_netex, qui sert à rattacher les tronçons."),
    'mnt_anglet': dict(title='MNT Anglet', mono='mnt.mnt_anglet', desc="Raster d'altitude", color='amber', x=0, y=380,
        text="Modèle numérique de terrain : il donne une altitude en tout point couvert par le raster. Il doit être dans un système de coordonnées compatible avec les couches vectorielles."),
    'tronons_de_cheminement': dict(title='Tronçons de cheminement', mono='troncon_cheminement', desc='geo_standards · lignes, from, to', color='coral', x=0, y=680,
        text="Table des tronçons (lignes) du réseau piéton. Les champs from et to désignent le nœud de départ et le nœud d'arrivée, par leur identifiant id_netex ; longueur donne la longueur du tronçon."),
}
ALG = {
 'rastersampling_1': dict(lane='A', step=1, title='Altitude des nœuds', tag='Prélèvement raster vers points', lines=[('MNT mnt_anglet · préfixe mnt_', 0)], chip='Nœuds avec altitude MNT',
    text="Lit l'altitude du MNT à la position de chaque nœud. La valeur est stockée dans un champ dont le nom commence par mnt_ (par exemple mnt_1)."),
 'joinattributestable_1': dict(lane='A', step=2, title='Altitude de départ', tag='Joindre par valeur de champ', lines=[('from = id_netex', 1), ('préfixe depart_', 0)], chip='Tronçons avec altitude de départ', badge=('coral', '+ Tronçons'),
    text="Rattache à chaque tronçon l'altitude de son nœud de départ : le champ from du tronçon est comparé à id_netex du nœud. Seule la première correspondance est retenue, et les tronçons sans correspondance sont conservés."),
 'joinattributestable_2': dict(lane='A', step=3, title="Altitude d'arrivée", tag='Joindre par valeur de champ', lines=[('to = id_netex', 1), ('préfixe arrivee_', 0)], chip='Tronçons avec altitudes MNT',
    text="Même jointure pour le nœud d'arrivée : le champ to du tronçon est comparé à id_netex. Les altitudes de départ et d'arrivée sont alors présentes sur chaque tronçon."),
 'fieldcalculator_1': dict(lane='A', step=4, title='Dénivelé', tag='Calculatrice de champ', lines=[('denivele_mnt =', 1), ('arrivee_mnt_1 − depart_mnt_1', 1)], chip='Tronçons avec dénivelé',
    text="Différence entre l'altitude du nœud d'arrivée et celle du nœud de départ, en mètres. Une valeur positive correspond à une montée dans le sens from vers to."),
 'fieldcalculator_2': dict(lane='A', step=5, title='Pente en %', tag='Calculatrice de champ', lines=[('pente_mnt = dénivelé ÷ longueur × 100', 0), ('NULL si la longueur est nulle ou absente', 0)], chip='Tronçons avec pente MNT',
    text="Pente moyenne du tronçon en pourcentage : dénivelé divisé par la longueur, multiplié par 100. Le calcul est protégé : si la longueur est absente ou nulle, la pente reste vide."),
 'pointsalonglines_1': dict(lane='B', step=1, title='Points le long des tronçons', tag="Points le long d'une géométrie", lines=[('un point tous les 5 m', 0), ('décalage début et fin : 1 m', 0)], chip='Points centraux pour le dévers',
    text="Place des points régulièrement sur chaque tronçon. Chaque point reçoit sa distance depuis le début du tronçon et l'angle de la ligne à cet endroit, deux informations utilisées ensuite pour placer les points latéraux."),
 'fieldcalculator_5': dict(lane='B', step=2, title='Identifiant du point', tag='Calculatrice de champ', lines=[('id_point = $id', 1)], chip='Points centraux (id_point)',
    text="Crée un identifiant numérique par point (id_point). Il servira de clé pour regrouper plus tard les altitudes de gauche et de droite d'un même point."),
 'fieldcalculator_3': dict(lane='B', step=3, title="Identifiant d'échantillon", tag='Calculatrice de champ', lines=[('id_echantillon =', 1), ('troncon_id_distance', 1)], chip='Points centraux identifiés',
    text="Compose un identifiant lisible à partir de l'identifiant du tronçon et de la distance du point sur ce tronçon."),
 'geometrybyexpression_2': dict(lane='B', step=4, title='Point gauche', tag='Géométrie par expression', lines=[("décalage de 0,5 m", 0), ("angle de l'axe − 90°", 0)], chip='Points latéraux gauche',
    text="Déplace chaque point de 0,5 m perpendiculairement à l'axe du tronçon, vers la gauche (angle de la ligne moins 90 degrés)."),
 'geometrybyexpression_3': dict(lane='B', step=4, title='Point droite', tag='Géométrie par expression', lines=[("décalage de 0,5 m", 0), ("angle de l'axe + 90°", 0)], chip='Points latéraux droite',
    text="Même déplacement de 0,5 m, vers la droite (angle de la ligne plus 90 degrés)."),
 'rastersampling_2': dict(lane='B', step=5, title='Altitude gauche', tag='Prélèvement raster vers points', lines=[('préfixe gauche_1', 0)], chip='Points gauche avec altitude', badge=('amber', '+ MNT'),
    text="Lit l'altitude du MNT à la position de chaque point de gauche."),
 'rastersampling_3': dict(lane='B', step=5, title='Altitude droite', tag='Prélèvement raster vers points', lines=[('préfixe droite_1', 0)], chip='Points droite avec altitude', badge=('amber', '+ MNT'),
    text="Lit l'altitude du MNT à la position de chaque point de droite."),
 'joinattributestable_3': dict(lane='B', step=6, title='Jointure transversale', tag='Joindre par valeur de champ', lines=[('clé : id_point', 1), ('préfixe joint_', 0)], chip='Points avec altitudes transversales',
    text="Rapproche, pour chaque point, l'altitude de gauche et celle de droite grâce à l'identifiant id_point. L'altitude de droite est recopiée avec le préfixe joint_ (joint_droite_11)."),
 'fieldcalculator_4': dict(lane='B', step=7, title='Dévers (dénivelé transversal)', tag='Calculatrice de champ', lines=[('denivele_transversal = droite − gauche', 1), ('NULL si une altitude manque', 0)], chip='Points avec dévers MNT',
    text="Écart d'altitude entre le point de droite et celui de gauche, en mètres. Les deux points étant distants de 1 m (0,5 m de part et d'autre de l'axe), multiplier la valeur par 100 donne un dévers approximatif en pourcentage. Si l'une des altitudes manque, le résultat reste vide."),
}
OUTPUTS = {
 'fieldcalculator_2': dict(id='out_pente', lane='A', title='Tronçons avec pente MNT', lines=["Altitudes de départ et d'arrivée,", 'dénivelé, pente en %'], color='A',
    text="Couche finale de la voie A : chaque tronçon avec les altitudes de ses extrémités, son dénivelé et sa pente."),
 'fieldcalculator_4': dict(id='out_devers', lane='B', title='Points avec dévers MNT', lines=["Un point tous les 5 m, à 0,5 m de l'axe,", 'avec le dénivelé transversal'], color='B',
    text="Couche finale de la voie B : des points le long des tronçons avec les altitudes de gauche et de droite et le dénivelé transversal."),
}
# ------------------------------------------------------------------ libellés des paramètres techniques
PLABEL = {'FIELD_NAME': 'Champ créé', 'FORMULA': 'Formule', 'EXPRESSION': 'Expression', 'PREFIX': 'Préfixe', 'COLUMN_PREFIX': 'Préfixe des colonnes',
          'DISTANCE': 'Distance entre points (m)', 'START_OFFSET': 'Décalage au début (m)', 'END_OFFSET': 'Décalage à la fin (m)',
          'METHOD': 'Méthode de jointure', 'DISCARD_NONMATCHING': 'Éliminer les non-correspondants', 'FIELD': 'Champ de la table d\'entrée',
          'FIELD_2': 'Champ de la table jointe', 'FIELDS_TO_COPY': 'Champs copiés'}
HIDE = {'FIELD_LENGTH', 'FIELD_PRECISION', 'FIELD_TYPE', 'OUTPUT_GEOMETRY', 'WITH_M', 'WITH_Z', 'INPUT', 'INPUT_2', 'RASTERCOPY', 'OUTPUT'}
CW, CH, IW, IH, OW, OH = 300, 150, 260, 110, 290, 100

def val(o):
    t = o.get('type')
    if t == 'Map': return {c.get('name'): val(c) for c in o}
    if t == 'List': return [val(c) for c in o]
    return o.get('value')

def fmt_param(name, items):
    items = items if isinstance(items, list) else [items]
    vals = []
    for it in items:
        if isinstance(it, dict):
            v = it.get('expression') if it.get('source') == '3' else it.get('static_value')
            if v is None: continue
            vals.append(str(v).strip().strip("'").strip())
        elif it is not None: vals.append(str(it))
    if not vals: return None
    v = ' ; '.join(vals)
    if name == 'METHOD': v = {'0': 'une ligne par correspondance', '1': 'première entité correspondante uniquement'}.get(v, v)
    if name == 'DISCARD_NONMATCHING': v = 'oui' if v.lower() == 'true' else 'non'
    return dict(label=PLABEL.get(name, name), value=v, mono=name in ('FIELD_NAME', 'FIELD', 'FIELD_2', 'FIELDS_TO_COPY', 'PREFIX', 'COLUMN_PREFIX'), pre=name in ('FORMULA', 'EXPRESSION'))

def build(model_path):
    d = val(ET.parse(model_path).getroot())
    ch = d['children']; nodes = []; edges = []
    for pname in d['parameters']:
        meta = INPUTS.get(pname, dict(title=pname, mono=pname, desc='', color='blue', x=40, y=40, text=''))
        nodes.append(dict(id=pname, kind='input', lane='E', title=meta['title'], mono=meta['mono'], desc=meta['desc'], text=meta['text'], color=meta['color'], x=meta['x'], y=meta['y'], w=IW, h=IH,
                          params=[dict(label='Paramètre du modèle', value=pname, mono=True)]))
    for cid, c in ch.items():
        short = cid.split(':')[-1]; m = ALG.get(short, {})
        lines = [dict(t=t, m=bool(mono)) for t, mono in m.get('lines', [])]
        params = [p for p in (fmt_param(n, v) for n, v in c['params'].items() if n not in HIDE) if p]
        outs = list((c.get('outputs') or {}).keys())
        nodes.append(dict(id=cid, kind='alg', lane=m.get('lane', 'A'), step=m.get('step'), title=m.get('title', c['component_description']), tag=m.get('tag', c['alg_id']), algo=c['alg_id'],
                          lines=lines, chip=m.get('chip', outs[0] if outs else ''), text=m.get('text', ''), params=params, color=m.get('lane', 'A'),
                          badge=dict(c=m['badge'][0], t=m['badge'][1]) if m.get('badge') else None,
                          x=float(c['component_pos_x']) - 100, y=float(c['component_pos_y']), w=CW, h=CH))
        for pn, pv in c['params'].items():
            for it in (pv if isinstance(pv, list) else [pv]):
                if not isinstance(it, dict): continue
                if it.get('source') == '1': edges.append(dict(**{'from': it['child_id'], 'to': cid, 'port': pn}))
                elif it.get('source') == '0': edges.append(dict(**{'from': it['parameter_name'], 'to': cid, 'port': pn}))
    pos = {n['id']: n for n in nodes}
    for src_short, o in OUTPUTS.items():
        sid = 'native:' + src_short
        if sid not in pos: continue
        s = pos[sid]
        nodes.append(dict(id=o['id'], kind='output', lane=o['lane'], title=o['title'], lines=[dict(t=t, m=False) for t in o['lines']], text=o['text'], color=o['color'],
                          x=s['x'] + CW + 90, y=s['y'] + (CH - OH) / 2, w=OW, h=OH, params=[]))
        edges.append(dict(**{'from': sid, 'to': o['id'], 'port': 'INPUT'}))
    nA = sum(1 for n in nodes if n['kind'] == 'alg')
    return dict(key=d.get('model_name') or 'etl', subtitle=f"Modèle QGIS · {len(d['parameters'])} entrées · {nA} traitements · 2 couches finales",
                nodes=nodes, edges=edges)

if __name__ == '__main__':
    if len(sys.argv) < 3: sys.exit(__doc__)
    data = build(sys.argv[1])
    html = open(sys.argv[2], encoding='utf-8').read()
    blob = json.dumps(data, ensure_ascii=False, indent=1).replace('</', '<\\/')
    new, n = re.subn(r'(<script id="etl-data" type="application/json">).*?(</script>)', lambda m: m.group(1) + blob + m.group(2), html, flags=re.S)
    if n != 1: sys.exit('Bloc <script id="etl-data"> introuvable dans le fichier HTML.')
    open(sys.argv[2], 'w', encoding='utf-8').write(new)
    print(f"OK : {len(data['nodes'])} cartes et {len(data['edges'])} liens écrits dans {sys.argv[2]}")
