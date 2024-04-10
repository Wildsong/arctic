<script>
    import MapList from './arcgis.svelte'
    //props 
    let viewDiv = "gallery";

</script>

<div>
    <h1>Gallery</h1>
    <div id={viewDiv} class="gallery">
    <MapList/>
    </div>
</div>

<style>
    .gallery {
		background-color: antiquewhite;
		display: flex;
		margin: 2px;
	}
</style>