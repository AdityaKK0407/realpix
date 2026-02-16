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
	<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
</svelte:head>

<section>
	<header></header>
	<slot />
</section>

<style>
	section {
		display: grid;
		grid-template-rows: 0.08fr 0.95fr;
		height: 100dvh;
		background-color: var(--color-bg-app);
		padding-inline: var(--app-padding-inline);
		padding-block: var(--app-padding-block);
	}
</style>
