# Documentation technique et méthodologique de l’AUDC51

<p align="center">
  <img width="1128" height="191" alt="Agence d'urbanisme du Pays de Châlons-en-Champagne" src="https://github.com/user-attachments/assets/caf61a4a-6e98-49f7-88a2-18da97dbc68f" />
</p>

<p align="center">
  <img width="587" height="320" alt="Capture d'écran 2026-10-13 095648" src="https://github.com/user-attachments/assets/6f565214-ca3c-46df-b05f-fba1fa537718" />
</p>

---

## Coordonnées

<p align="center">
  📍 <strong>Adresse :</strong> <a href="https://www.google.com/maps/search/?api=1&query=26+rue+Joseph-Marie+Jacquard+51000+Ch%C3%A2lons-en-Champagne" target="_blank">26 rue Joseph-Marie Jacquard, 51000 Châlons-en-Champagne</a>
  <br>
  ✉️ <strong>Mail :</strong> <a href="mailto:audcchalons@gmail.com">audcchalons@gmail.com</a>
  <br>
  💬 <a href="https://www.audc51.org/contact/" target="_blank">Nous contacter</a>
  <br>
  👥 <a href="https://www.audc51.org/lagence/lequipe-technique/" target="_blank">Équipe</a>
</p>

<div align="center">
<button id="avis-open" type="button" style="padding: 8px 18px; background-color: #c8187a; color: #ffffff; border: none; border-radius: 6px; font-weight: bold; cursor: pointer;">💡 Une remarque, une suggestion ?</button>
<dialog id="avis-dialog" style="border: 1px solid #c8187a; border-radius: 10px; padding: 20px; width: 90%; max-width: 480px; text-align: left;">
<form id="avis-form">
<h3 style="margin-top: 0; color: #c8187a;">Donner votre avis</h3>
<input type="text" name="Page concernée" placeholder="Page concernée (facultatif)" style="width: 100%; box-sizing: border-box; padding: 8px; margin-bottom: 10px;">
<textarea name="Remarque" required rows="6" placeholder="Votre remarque ou suggestion" style="width: 100%; box-sizing: border-box; padding: 8px; margin-bottom: 10px;"></textarea>
<input type="hidden" name="_subject" value="Documentation AUDC 51 - Suggestion">
<input type="hidden" name="_captcha" value="false">
<input type="text" name="_honey" style="display: none;">
<button type="submit" style="padding: 8px 18px; background-color: #c8187a; color: #ffffff; border: none; border-radius: 6px; font-weight: bold; cursor: pointer;">Envoyer</button>
<button type="button" id="avis-close" style="padding: 8px 18px; margin-left: 6px; border: 1px solid #cccccc; border-radius: 6px; background: #ffffff; cursor: pointer;">Annuler</button>
<p id="avis-status" style="margin-bottom: 0;"></p>
</form>
</dialog>
</div>
<script>
(function () {
  var d = document.getElementById('avis-dialog');
  var s = document.getElementById('avis-status');
  document.getElementById('avis-open').onclick = function () { s.textContent = ''; d.showModal(); };
  document.getElementById('avis-close').onclick = function () { d.close(); };
  document.getElementById('avis-form').onsubmit = function (e) {
    e.preventDefault();
    var form = e.target;
    s.textContent = 'Envoi en cours...';
    fetch('https://formsubmit.co/ajax/guenelahad@gmail.com', {
      method: 'POST',
      headers: { 'Accept': 'application/json' },
      body: new FormData(form)
    })
    .then(function (r) { return r.json(); })
    .then(function (data) {
      if (data.success === 'true' || data.success === true) {
        s.textContent = 'Merci, votre message a bien été envoyé !';
        form.reset();
      } else { throw new Error('echec'); }
    })
    .catch(function () { s.textContent = "Erreur d'envoi, veuillez réessayer."; });
  };
})();
</script>

## Objectifs de la plateforme

Site développé dans le cadre de l’amélioration continue des outils de l’agence.

Ce site rassemble l’ensemble des ressources, méthodes et bonnes pratiques utilisées pour la production, la gestion et l’analyse des données géomatiques. Il a été conçu pour offrir un cadre clair, structuré et facilement accessible aux agents et partenaires travaillant sur des projets SIG.

- Centraliser les connaissances et les outils, notamment en géomatique.
- Améliorer l’accès aux données, aux procédures et aux référentiels.
- Garantir la qualité, la traçabilité et la cohérence des traitements.
- Faciliter le partage d’informations entre les différents projets.
- Servir de guide aux nouveaux utilisateurs des outils SIG.

## Sites de l'Agence

[🔗 Site officiel de l'AUDC51](https://www.audc51.org/)

[🔗 Tableau de bord des travaux cartographiques en lien avec la future base de données](https://audcchalons51.github.io/tableau-de-bord-etudes-carto-audc51/)

[🔗 LinkedIn](https://www.linkedin.com/company/agence-d-urbanisme-de-ch%C3%A2lons-en-champagne-audc/posts/)

*D’autres rubriques seront ajoutées progressivement : base de données, GDAL, télédétection, traitements Python, métadonnées, etc.*

<p align="center">
  <img width="1200" height="333" alt="Expertise technique : QGIS, ArcGIS, webmapping, serveur - CartoExpert" src="https://github.com/user-attachments/assets/0dc750dc-c27c-45fd-87a3-da3f37b33c5a" />
</p>
