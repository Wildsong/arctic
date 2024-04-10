<script>
    import {onMount} from "svelte";
    import {loadModules} from "esri-loader";

    // props

    let viewDiv = "arcgis_map";
    let username = "login";
    let stuff = "";

    // wait until the esri component has loaded
    // see https://svelte.dev/tutorial/onmount
    onMount(async() => {
        const esriLoaderOptions = {
            css: true
        };

        // In a "normal" world these would be "imports"
        const [
            Portal,
            PortalUser,
            PortalQueryParams,
            esriConfig,
        ] = await loadModules([
                'esri/portal/Portal',
                'esri/portal/PortalUser',
                'esri/portal/PortalQueryParams',
                'esri/config', 
            ],
            esriLoaderOptions
        );
        const pu = new PortalUser({
            username: "bwilson@CLATSOP",
        });
        const portal = new Portal({
            url: "https://delta.co.clatsop.or.us/portal",
            user: pu,
        }
        );
//        portal.authMode = 'immediate';
        let queryParams = new PortalQueryParams({
            query: '1=1',
            num: 100
        });
        username = portal.user.username;
        portal.queryItems(queryParams).then(createGallery);
        console.log('My portal connection:', portal);
    })

    const createGallery = (items) => {
        //console.log("Items: ", items);
        let results = items.results;
        stuff = results.length + ' Results'
        stuff += '<ul>';
        for (i in results) {
            let item = results[i]
            console.log(item)
            stuff += '<li>' + item.id + ' ' + item.title ;
        }
        stuff += '</ul>';
    };
</script>

<div>
    <h1>ArcGIS JSAPI 4</h1>
    <div id={viewDiv} class="apps" bind:this={viewDiv}>'
        {username}
        {@html stuff}
    </div>
</div>