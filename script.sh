sudo apt update
sudo apt install -y curl 
sudo apt install -y unzip

curl -fsSL https://fnm.vercel.app/install | bash
source ~/.bashrc
fnm use --install-if-missing 20
node -v
npm -v

npm install -g @vue/cli

pip install Flask
pip install Flask-CORS
pip install psutil

npm install

#npm run build
#npm install -g http-server
#http-server --port 7000