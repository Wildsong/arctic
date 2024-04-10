<script>
	import Gallery from './gallery.svelte'
	const logoUrl = new URL('../assets/logo.png', import.meta.url);
</script>

<main>
	<div class="header">
		<img alt="logo" src="{logoUrl}" width=120 height=120 />
		home
		gallery
		content
		organization
		sign in
	</div>

	<Gallery />

	<div class="footer">
		<p>
			GIS Services, a division of the Department of Information Services
		</p>
		<p>
			<a href="tel:503-338-3668">Call us</a>
		</p>
	</div>
</main>

<style>
	main {
		padding: 1em;
		margin: 0 auto;
	}
	.footer {
		background-color: azure;
		width: 800px;
	}
	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>