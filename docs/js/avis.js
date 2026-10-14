(function () {
  // --- Styles (bouton flottant + fenêtre) ---
  var css = document.createElement('style');
  css.textContent =
    '#avis-open{position:fixed;bottom:16px;left:16px;z-index:9999;padding:10px 16px;' +
    'background:#c8187a;color:#fff;border:none;border-radius:24px;font-weight:bold;' +
    'cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.3);font-size:14px;}' +
    '#avis-open:hover{background:#a01262;}' +
    '@media screen and (min-width:769px){#avis-open{left:316px;}}' +
    '#avis-dialog{border:1px solid #c8187a;border-radius:10px;padding:20px;width:90%;' +
    'max-width:480px;text-align:left;}' +
    '#avis-dialog::backdrop{background:rgba(0,0,0,.4);}' +
    '#avis-dialog h3{margin-top:0;color:#c8187a;}' +
    '#avis-dialog input[type=text],#avis-dialog textarea{width:100%;box-sizing:border-box;' +
    'padding:8px;margin-bottom:10px;}' +
    '#avis-dialog .avis-btn{padding:8px 18px;border:none;border-radius:6px;font-weight:bold;cursor:pointer;}' +
    '#avis-status{margin:10px 0 0;}';
  document.head.appendChild(css);

  // --- Bouton + fenêtre ---
  var wrap = document.createElement('div');
  wrap.innerHTML =
    '<button id="avis-open" type="button">💡 Une remarque ou suggestion ?</button>' +
    '<dialog id="avis-dialog"><form id="avis-form">' +
    '<h3>Donner votre avis</h3>' +
    '<input type="text" name="Page concernée" id="avis-page" placeholder="Page concernée">' +
    '<textarea name="Remarque" required rows="6" placeholder="Votre remarque ou suggestion"></textarea>' +
    '<input type="hidden" name="_subject" value="Documentation AUDC 51 - Suggestion">' +
    '<input type="hidden" name="_captcha" value="false">' +
    '<input type="text" name="_honey" style="display:none">' +
    '<button type="submit" class="avis-btn" style="background:#c8187a;color:#fff;">Envoyer</button> ' +
    '<button type="button" id="avis-close" class="avis-btn" style="background:#eee;color:#333;">Annuler</button>' +
    '<p id="avis-status"></p></form></dialog>';
  document.body.appendChild(wrap);

  var d = document.getElementById('avis-dialog');
  var s = document.getElementById('avis-status');

  document.getElementById('avis-open').onclick = function () {
    document.getElementById('avis-page').value = document.title;  // page préremplie
    s.textContent = '';
    d.showModal();
  };
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
