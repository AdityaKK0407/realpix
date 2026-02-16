<script lang="ts">
	import { Bot, Shield } from 'lucide-svelte';
	import { fileUploadFooterData } from '$lib/data/FileUploadingMetrics.data';
	import { turnstileSetup } from '$lib/state/turnstile.store';
	import { onDestroy } from 'svelte';
	import { browser } from '$app/environment';

	const elementProps = {
		size: '27',
		strokeWidth: 1
	};

	let turnstileContainer: HTMLDivElement; // Reference to the div where Turnstile will be rendered
	let turnstileWidgetId: string | undefined;

	function handleTurnstileSuccess(token: string) {
		console.log('Turnstile success:', token);
		turnstileSetup.set('verified');
	}

	// Reactive statement to render Turnstile when not verified, ONLY in the browser
	$: if (browser && $turnstileSetup === 'not-verified' && turnstileContainer) {
		// Wait for the Turnstile script to be loaded
		const interval = setInterval(() => {
			if (window.turnstile) {
				clearInterval(interval);
				if (turnstileWidgetId) {
					window.turnstile.remove(turnstileWidgetId); // Remove existing widget if any
				}
				turnstileWidgetId = window.turnstile.render(turnstileContainer, {
					sitekey: 'SITE_KEY',
					callback: handleTurnstileSuccess,
					theme: 'light',
					size: 'normal'
				});
			}
		}, 100); // Check every 100ms
	}

	// Clean up Turnstile widget when component is destroyed
	onDestroy(() => {
		if (browser && turnstileWidgetId && window.turnstile) {
			window.turnstile.remove(turnstileWidgetId);
		}
	});
</script>

<section class="displaySection">
	{#each fileUploadFooterData as metric (metric.id)}
		{#if $turnstileSetup === 'verified'}
			<div class="fieldSection">
				<div
					class="iconField"
					class:blue={metric.color === 'blue'}
					class:green={metric.color === 'green'}
				>
					{#if metric.icon === 'Ai'}
						<Bot {...elementProps} stroke="currentColor" strokeWidth={2} />
					{:else if metric.icon === 'Shield'}
						<Shield {...elementProps} fill="currentColor" />
					{/if}
				</div>
				<div class="text-wrapper">
					<p class="sm-font-1">{metric.heading}</p>
					<p class="sm-font-2 bold">{metric.text}</p>
				</div>
			</div>
		{:else}
			<div class="cf-turnstile" bind:this={turnstileContainer}></div>
		{/if}
	{/each}
</section>

<style>
	.displaySection {
		display: flex;
		--spacing: 0.8rem;
		--internal-spacing: 0.4rem;
		gap: var(--spacing);
	}

	.fieldSection {
		border: 0.12rem solid rgba(0 0 0 / 0.08);
		display: flex;
		gap: var(--internal-spacing);
		padding: var(--small-padding);
		border-radius: 0.9rem;
		align-items: center;
	}

	.text-wrapper {
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
</style>
