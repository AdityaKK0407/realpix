<script lang="ts">
	import { resolve } from '$app/paths';
</script>

<svelte:head><title>Home</title></svelte:head>

<section>
	<header>
		<h1>RealPix</h1>
	</header>
	<main>
		<p>Hello</p>
		<a href={resolve('/imageUpload')}>Image</a>
	</main>
</section>

<style>
	header {
		grid-row-start: 1;
	}
</style>
