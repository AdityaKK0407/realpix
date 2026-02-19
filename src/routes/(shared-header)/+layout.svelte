<script lang="ts">
	import '$lib/css/variables.css';
	import '$lib/css/styles.css';
	import '$lib/css/utilities.css';
</script>

<svelte:head>
	<link
		rel="stylesheet"
		href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&icon_names=image_inset"
	/>
	<script
		src="https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit"
		async
		defer
	></script>
</svelte:head>

<section>
	<header>
		<h1>RealPix</h1>
	</header>
	<slot />
</section>

<style>
	section {
		display: grid;
		grid-template-rows: 0.085fr 0.845fr 0.07fr;
		height: 100dvh;
		background-color: var(--color-bg-app);
		padding-inline: var(--app-padding-inline);
		padding-block: var(--app-padding-block);
	}

	header {
		grid-row-start: 1;
	}
</style>
