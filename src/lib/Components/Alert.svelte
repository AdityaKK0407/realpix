<script lang="ts">
	import { Check, CircleX, Info, TriangleAlert } from 'lucide-svelte';
	import { cubicInOut } from 'svelte/easing';
	import { Tween } from 'svelte/motion';

	interface Props {
		alertType: 'info' | 'warning' | 'critical' | 'cloudfare-error' | 'success' | 'pasting-accept';
		heading: string;
		body: string;
		animating: boolean;
	}
	const props: Props = $props();
	let progress = new Tween(0, {
		duration: 500,
		easing: cubicInOut,
		delay: 25
	});
	let progressValue = 0;

	function simulateUpload() {
		const interval = setInterval(() => {
			if (progressValue >= 100) {
				progressValue = 0;
				progress.set(1);
				clearInterval(interval);
			} else {
				progressValue += 5;
				progress.set(progressValue / 100);
			}
		}, 250);
	}

	if (props.animating) {
		simulateUpload();
	}
</script>

<section
	class="alert"
	class:info={props.alertType === 'info'}
	class:warning={props.alertType === 'warning'}
	class:critical={props.alertType === 'critical'}
	class:success={props.alertType === 'success'}
>
	<section
		class="alert__progress"
		aria-label="This element is the progress used for closing the alert."
	>
		<div class="alert__progress__fill" style="--progress-value: {progress.current}"></div>
	</section>
	<section class="alert__information">
		<div class="alert__icon flex">
			{#if props.alertType === 'info'}
				<Info size="32" stroke="currentColor" />
			{:else if props.alertType === 'warning'}
				<TriangleAlert size="32" stroke="currentColor" />
			{:else if props.alertType === 'critical'}
				<span class="material-symbols-outlined dangerIcon"> dangerous </span>
			{:else if props.alertType === 'success'}
				<Check size="32" stroke="currentColor" />
			{/if}
		</div>
		<section class="alert__content">
			<p class="bolder sm-font-5 alert__content__heading">{props.heading}</p>
			<p class="sm-font-2">{props.body}</p>
		</section>
		<button class="alert__close__btn flex" aria-label="Click the button to close the alert">
			<CircleX />
		</button>
	</section>
</section>

<style>
	.alert {
		display: grid;
		background-color: var(--color-warm-gray);
		border-radius: 1rem;
		--box-shadow-values: 0 0.3rem 0.9rem 0.45rem;
		position: absolute;
		top: 1rem;
		right: 1.7rem;
		overflow: auto;
	}

	.info {
		box-shadow: var(--box-shadow-values) var(--color-primary-200);
		color: var(--color-primary);
		--background-color: var(--color-primary-lowest);
		--progress-color: var(--color-primary);
	}

	.warning {
		box-shadow: var(--box-shadow-values) var(--color-warning-200);
		color: var(--color-warning);
		--background-color: var(--color-warning-lowest);
	}

	.critical {
		box-shadow: var(--box-shadow-values) var(--color-error-200);
		color: var(--color-error);
		--background-color: var(--color-error-lowest);
	}

	.success {
		box-shadow: var(--box-shadow-values) var(--color-success-200);
		color: var(--color-success-green);
		--background-color: var(--color-success-lowest);
		--progress-color: var(--color-success-green);
	}

	.alert__information {
		display: flex;
		padding: var(--medium-padding);
		gap: var(--text-gap);
		grid-row-start: 1;
	}

	.alert__progress {
		width: 100%;
		height: 0.2rem;
		background: transparent;
		grid-row-start: 2;
		position: relative;
	}

	.alert__progress__fill {
		position: absolute;
		left: 0;
		top: 0;
		width: 100%;
		height: 100%;
		background-color: var(--progress-color);
		border-radius: 1rem;
		will-change: transform;
		transform: scaleX(var(--progress-value));
		transform-origin: left;
		transition: transform 500ms ease-in-out;
	}

	.alert__icon {
		grid-row-start: 1;
		background-color: var(--background-color);
		border-radius: 50vw;
		align-items: center;
		justify-content: center;
		padding: var(--small-padding);
	}

	.dangerIcon {
		font-size: 2rem;
	}

	.alert__content {
		grid-row-start: 1;
	}

	.alert__content__heading {
		letter-spacing: 0.01em;
	}

	.alert__close__btn {
		grid-row-start: 1;
		align-self: flex-start;
		padding: var(--small-padding);
		align-items: center;
		justify-content: center;
		border-radius: 1.4rem;
		background-color: transparent;
	}
</style>
