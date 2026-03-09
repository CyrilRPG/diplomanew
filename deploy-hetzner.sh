#!/usr/bin/env bash
# Déploie le dossier diploma (Desktop) vers Hetzner et redémarre l'app pour actualiser le site.
# Usage : ./deploy-hetzner.sh
# Les fichiers sont envoyés vers /var/www/diploma (répertoire servi par le site).

set -e
SERVER="root@91.107.213.199"
# Répertoire live du site sur le serveur (celui servi par Node/PM2)
REMOTE_DIR="/var/www/diploma"
# Nom du processus PM2 qui sert le site (vérifier avec: ssh ... "pm2 list")
APP_NAME="server"

echo "=== 1. Synchronisation des fichiers vers $SERVER:$REMOTE_DIR ==="
rsync -avz --delete \
  --exclude='.git' \
  --exclude='node_modules' \
  --exclude='revokedTokens.json' \
  ./ "$SERVER:$REMOTE_DIR/"

# Nginx utilise aussi root /var/www/html pour flashcard.diploma-sante.fr → on met à jour les deux
echo ""
echo "=== 1b. Synchronisation vers /var/www/html (dossier servi par Nginx) ==="
rsync -avz --delete \
  --exclude='.git' \
  --exclude='node_modules' \
  --exclude='revokedTokens.json' \
  ./ "$SERVER:/var/www/html/"

echo ""
echo "=== 2. Relance de l'app depuis $REMOTE_DIR (PM2) ==="
# Restart garde l'ancien répertoire de travail ; on supprime et on relance depuis REMOTE_DIR pour servir les bons fichiers.
ssh "$SERVER" "cd $REMOTE_DIR && pm2 delete $APP_NAME 2>/dev/null; pm2 delete diploma-server 2>/dev/null; pm2 start server.js --name $APP_NAME && pm2 save"

echo ""
echo "=== 3. Diagnostic (pourquoi le site ne change peut-être pas) ==="
ssh "$SERVER" 'echo "--- Répertoire de travail du processus server ---" && pm2 show server 2>/dev/null | grep -E "exec cwd|script path" || true
echo ""
echo "--- Nginx : quel répertoire ou proxy est utilisé pour le site ? ---"
if command -v nginx >/dev/null 2>&1; then nginx -T 2>/dev/null | grep -E "root |proxy_pass|server_name" | head -20; else echo "Nginx non trouvé"; fi
echo ""
echo "--- Réponse du serveur Node sur le port 3000 (premières lignes) ---"
curl -s -m 2 http://127.0.0.1:3000/ 2>/dev/null | head -3 || echo "Aucune réponse sur :3000"
echo ""
echo "--- Contenu de /var/www (où pointe le site ?) ---"
ls -la /var/www/ 2>/dev/null' || true

echo ""
echo "=== Déploiement terminé. ==="
echo "Si le site ne change toujours pas : Nginx sert peut-être un autre dossier (ex. /var/www/html)."
echo "Vérifiez la section « Nginx » ci-dessus : si vous voyez « root /var/www/html », il faut soit"
echo "  - déployer aussi vers ce dossier, soit configurer Nginx pour proxy_pass vers http://127.0.0.1:3000"
