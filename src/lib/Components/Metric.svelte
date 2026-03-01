<script lang="ts">
	import { range, utils } from '$lib/scripts/utils';
	import ShieldSvg from '$lib/Svg/ShieldSvg.svelte';
	import type { IconNames, IconTypes } from '$lib/types/fileupload.types';
	import { Bot, Shield } from 'lucide-svelte';
	interface Props {
		iconName: IconNames;
		heading: string;
		text: string;
		animate?: boolean;
		iconType: IconTypes;
	}

	const props: Props = $props();
	const elementProps = {
		size: '35'
	};
	const condition = utils.performAnimation(props.iconType);
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
			class:removePadding={props.iconType.includes('animated')}
			class:animate={condition}
			class:noAnimate={!condition}
			class:yellow={utils.returnColorForType(props.iconType) === 'yellow'}
			class:red={utils.returnColorForType(props.iconType) === 'red'}
			class:periwinkle={utils.returnColorForType(props.iconType) === 'periwinkle'}
			class:gray={utils.returnColorForType(props.iconType) === 'gray'}
			class:blue={utils.returnColorForType(props.iconType) === 'blue'}
			class:green={utils.returnColorForType(props.iconType) === 'green'}
			class:security-green={utils.returnColorForType(props.iconType) === 'security-green'}
		>
			{#if props.iconName === 'Ai'}
				<Bot {...elementProps} stroke="currentColor" strokeWidth={2} />
			{:else if props.iconType === 'security-animated'}
				<ShieldSvg />
			{:else if props.iconName === 'Shield'}
				<Shield {...elementProps} stroke="currentColor" strokeWidth={2} />
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

	.animate {
		--layer-0-time: 7s;
		--other-layers-time: 4s;
	}

	.noAnimate {
		--layer-0-time: 0s;
		--other-layers-time: 0s;
	}

	.yellow {
		--shield-svg-color: var(--color-yellow);
	}

	.periwinkle {
		--shield-svg-color: var(--color-primary);
	}

	.red {
		--shield-svg-color: var(--color-error);
	}

	.gray {
		--shield-svg-color: var(--color-text-muted);
	}

	.security-green {
		--shield-svg-color: var(--color-success-green);
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
