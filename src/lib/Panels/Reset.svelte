<script lang="ts">
	import { Image } from 'lucide-svelte';

	interface Props {
		text: string[];
	}

	let props: Props = $props();
</script>

<section class="mainSection">
	<section class="wrapper flex-column">
		<div class="color-pri">
			<Image size="75" />
		</div>

		<section class="flex-column display-text">
			{#each props.text as line (line)}
				<p class="md-font-2 bold">{line}</p>
			{/each}
		</section>
	</section>
</section>

<style>
	.mainSection {
		flex-grow: 1;
		display: grid;
		grid-template-rows: 1fr 0.5fr;
		grid-template-columns: 0.5fr 0.7fr 0.5fr;
		align-items: center;
	}

	.wrapper {
		grid-column-start: 2;
		justify-content: center;
		align-items: center;
		gap: 1rem;
		color: var(--color-text-body);
		background-color: var(--color-primary-lowest);
		padding: var(--medium-padding);
		border-radius: 1.2rem;
	}

	section div {
		display: flex;
		align-items: center;
		padding: var(--small-padding);
		border-radius: 50vw;
	}

	.display-text {
		gap: 0.13rem;
		align-items: center;
	}
</style>
