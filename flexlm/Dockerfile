FROM mcr.microsoft.com/windows/server:ltsc2022-amd64
SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop';$ProgressPreference='silentlyContinue';"]

WORKDIR C:/srv

ADD https://nodejs.org/dist/latest-v21.x/node-v21.7.3-win-x64.zip nodejs.zip
RUN Expand-Archive nodejs.zip -DestinationPath .
RUN Rename-Item node-v21.7.3-win-x64 nodejs
# This appends to the existing PATH
RUN del nodejs.zip
RUN SETX PATH C:/srv/nodejs

 # HTTP, WS
EXPOSE 4000
# HTTPS, WSS
EXPOSE 4001

RUN npm config set registry https://registry.npmjs.org/

# This creates a package.json file and adds 'express' to it
# I used this as a starting point then switched to using a package.json in the sources
#RUN npm init -y; npm install express
#COPY app .
#ENTRYPOINT ["node"]
#CMD ["app/app.js"]

# This is the development version with reload
ADD package.json .
RUN npm install

ADD lmstat.bat .
ADD service.txt .

#CMD ["npm", "app/app.js"]
