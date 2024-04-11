FROM mcr.microsoft.com/windows/server:ltsc2022-amd64
SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop';$ProgressPreference='silentlyContinue';"]

WORKDIR C:/srv

#ADD https://nodejs.org/dist/latest-v21.x/node-v21.7.3-win-x64.zip nodejs.zip
#RUN Expand-Archive nodejs.zip -DestinationPath C:/srv/.
#RUN Rename-Item node-v21.7.3-win-x64 nodejs

#EXPOSE 3000

RUN SETX PATH C:/srv/nodejs
#RUN npm config set registry https://registry.npmjs.org/

ADD lmstat.bat .
ADD service.txt .

# This is a shortcut that creates a package.json file and adds 'express'
#RUN npm init -y; npm install express
#COPY app.js .
ENTRYPOINT ["cmd"]
CMD ["lmstat.bat"]
