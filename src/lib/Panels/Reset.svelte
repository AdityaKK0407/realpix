<script lang="ts">
	import { Image } from 'lucide-svelte';

	interface Props {
		text: string[];
		serverStatus: boolean;
		inactiveText: string[];
	}

	let props: Props = $props();
</script>

<section class="mainSection">
	<section class="wrapper flex-column">
		<div class="color-pri">
			<Image size="50" />
		</div>

		{#if props.serverStatus}
			<section class="flex-column display-text">
				{#each props.text as line (line)}
					<p class="md-font-1 bold">{line}</p>
				{/each}
			</section>
		{:else if !props.serverStatus}
			<p>{props.inactiveText[0]}</p>
		{/if}
	</section>
</section>

<style>
	.mainSection {
		flex-grow: 1;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.wrapper {
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
