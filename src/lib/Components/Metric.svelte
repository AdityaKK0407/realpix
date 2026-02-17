<script lang="ts">
	import { range } from '$lib/scripts/utils';
	import type { Colors, IconNames } from '$lib/types/fileupload.types';
	import { Bot, Shield, Server } from 'lucide-svelte';
	interface Props {
		iconName: IconNames;
		heading: string;
		text: string;
		color: Colors;
		animate?: boolean;
	}

	const props: Props = $props();
	const elementProps = {
		size: '27',
		strokeWidth: 1
	};
</script>

<div class="fieldSection" class:fieldSection__pulse={props.animate}>
	{#if props.animate}
		{#each range(1, 5) as number (number)}
			<span style={`--i:${number}`} class="fieldSection__animateElement"></span>
		{/each}
	{/if}
	<section class="flex fieldSection__content">
		<div
			class="iconField"
			class:blue={props.color === 'blue'}
			class:green={props.color === 'green'}
			class:orange={props.color === 'orange'}
		>
			{#if props.iconName === 'Ai'}
				<Bot {...elementProps} stroke="currentColor" strokeWidth={2} />
			{:else if props.iconName === 'Shield'}
				<Shield {...elementProps} fill="currentColor" />
			{:else if props.iconName === 'Server'}
				<Server {...elementProps} fill="currentColor" />
			{/if}
		</div>
		<div class="fieldSection__text">
			<p class="sm-font-1">{props.heading}</p>
			<p class="sm-font-2 bold">{props.text}</p>
		</div>
	</section>
</div>

<style>
	.fieldSection {
		border: 0.12rem solid rgba(0 0 0 / 0.08);
		display: flex;
		gap: var(--internal-spacing);
		padding: var(--small-padding);
		border-radius: 0.9rem;
		align-items: center;
		background-color: var(--color-bg-surface);
	}

	.fieldSection__content {
		gap: var(--internal-spacing);
		position: relative;
		z-index: 2;
	}

	.fieldSection__text {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.blue {
		background-color: var(--color-primary-100);
		filter: drop-shadow(0 0 0.5rem var(--color-primary-300));
		color: var(--color-primary-900);
	}

	.green {
		background-color: var(--color-success-100);
		filter: drop-shadow(0 0 0.5rem var(--color-success-300));
		color: var(--color-success-900);
	}

	.orange {
		background-color: var(--color-warning-100);
		filter: drop-shadow(0 0 0.5rem var(--color-warning-300));
		color: var(--color-warning-900);
	}

	.fieldSection__pulse {
		display: grid;
	}

	.fieldSection__pulse > * {
		grid-row-start: 1;
		grid-column-start: 1;
	}

	.fieldSection__pulse > .fieldSection__animateElement {
		width: 100%;
		height: 100%;
		background-color: var(--color-warning-500);
		border-radius: 0.9rem;
		animation: animate 3s ease-out infinite;
		animation-delay: calc(var(--i) * -1.2s);
		z-index: -1;
	}

	@keyframes animate {
		0% {
			scale: 1.2;
			opacity: 0.5;
		}
		50% {
			opacity: 0.45;
		}
		75% {
			opacity: 0.35;
		}
		100% {
			scale: 1.5 1.85;
			opacity: 0;
		}
	}
</style>
