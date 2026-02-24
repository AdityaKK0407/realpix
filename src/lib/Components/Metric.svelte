<script lang="ts">
	import { range } from '$lib/scripts/utils';
	import { turnstile } from '$lib/state/turnstile.svelte';
	import type { Colors, IconNames } from '$lib/types/fileupload.types';
	import { Bot, Shield } from 'lucide-svelte';
	interface Props {
		iconName: IconNames;
		heading: string;
		text: string;
		color: Colors;
		animate?: boolean;
		turnstileSupport?: boolean;
	}

	const props: Props = $props();
	const elementProps = {
		size: '27',
		strokeWidth: 1
	};
	const condition = props.heading === 'Encryption';
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
			class:security={condition &&
				props.turnstileSupport &&
				turnstile.getStatus() === 'not-verified'}
			class:security_verified={condition &&
				props.turnstileSupport &&
				turnstile.getStatus() === 'verified'}
			class:security_setup={condition && props.turnstileSupport}
			class:blue={props.color === 'blue'}
			class:green={props.color === 'green' && props.heading !== 'Encryption'}
			class:orange={props.color === 'orange'}
		>
			{#if props.iconName === 'Ai'}
				<Bot {...elementProps} stroke="currentColor" strokeWidth={2} />
			{:else if props.iconName === 'Shield'}
				<Shield {...elementProps} fill="currentColor" />
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
		gap: var(--text-gap-small);
	}

	.security {
		color: var(--color-text-muted);
		opacity: 0.4;
		background-color: transparent;
	}

	.security_setup {
		transition:
			color 450ms cubic-bezier(0.66, 0, 0.34, 1),
			opacity 350ms ease-in-out,
			background-color 350ms cubic-bezier(0.78, 0, 0.22, 1);
	}

	.security_verified {
		color: var(--color-success-green);
		opacity: 1;
		background-color: var(--color-success-100);
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
		animation-delay: calc(var(--i) * -1.5s);
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
