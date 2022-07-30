# arctic home

Replacement for standard ArcGIS Server Portal page.

## Requirements

* Branding consistent with our public web site
* Navbar that give access to Portal components.
* Sign in.
* Applications available to public (or signed in user)
* Services available to public (or signed in user)
* Standard footer

## Implementation goals

* Svelte App
* Uses Esri JSAPI to access Portal services
* 100% Typescript (as soon as I learn it)

## Get started

Install the dependencies. 

```bash
npm install
```

Then start it. This should automatically open a browser and connect it to http://localhost:1234
If not, something is wrong; maybe you don't have Chrome or something.

```bash
npm start
```

You should see the home page.

![alt text](screenshots/home.png "Screenshot of app running in Chrome.")

## Deploying to the web

The Svelte people suggest using Vercel.com or Surge.sh;
probably both fine ideas but I want to keep the content in my own servers.
To me the bundler is there to make deployment simple, so "copy" is a good way to deploy too.

I think for me it's perhaps just an rsync command.

```bash
npm run build
rsync -av dist/* cc-testmaps:docker/nginx/html
```

I have that automated with

```bash
npm run deploy
```

You of course, would have to edit package.json to change the rsync
command because you can't deploy to my server.

## Additional help

I was inspired by a presentation from the Esri Dev Summit.
The original presentation is on YouTube, <https://www.youtube.com/watch?v=Y_EVrWtBnow>

* <https://esri-svelte-basemaps-example.now.sh/>
* <https://github.com/jwasilgeo/esri-svelte-basemaps-example>

JSAPI reference: <https://developers.arcgis.com/javascript/latest/api-reference/>

Blog: <https://odoe.net/blog/svelte-with-the-arcgis-api-for-javascript/>

