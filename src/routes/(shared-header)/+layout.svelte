<script lang="ts">
	import '$lib/css/variables.css'
	import '$lib/css/styles.css'
	import '$lib/css/utilities.css'
</script>

<section>
	<header></header>
	<slot />
</section>

<style>
	section {
			display: grid;
			grid-template-rows: 0.15fr 0.85fr;
			height: 100dvh;
			background-color: var(--color-bg-app);
			padding-inline: var(--app-padding-inline);
			padding-block: var(--app-padding-block);
	}
</style>