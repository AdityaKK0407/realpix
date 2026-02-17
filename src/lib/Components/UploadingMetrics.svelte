<script lang="ts">
	import { fileUploadFooterData } from '$lib/data/FileUploadingMetrics.data';
	import { turnstileSetup } from '$lib/state/turnstile.store';
	import { onDestroy, onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { PUBLIC_TURNSTILE_SITE_KEY } from '$env/static/public';
	import { type ServerStatus } from '$lib/types/fileupload.types';
	import Metric from './Metric.svelte';

	let turnstileContainer: HTMLDivElement | null = $state(null); // Reference to the div where Turnstile will be rendered
	let turnstileWidgetId: string | undefined;
	let serverStatus: ServerStatus = $state('InActive');

	function handleTurnstileSuccess(token: string) {
		alert('Turnstile success:');
		alert(token);
		turnstileSetup.set('verified');
	}

	onMount(() => {
		if (browser && $turnstileSetup === 'not-verified') {
			const checkTurnstile = setInterval(() => {
				if (window.turnstile && turnstileContainer) {
					clearInterval(checkTurnstile);
					turnstileWidgetId = window.turnstile.render(turnstileContainer, {
						sitekey: PUBLIC_TURNSTILE_SITE_KEY,
						callback: handleTurnstileSuccess,
						theme: 'light',
						size: 'normal'
					});
				}
			}, 100);

			return () => clearInterval(checkTurnstile);
		}
	});

	// Clean up Turnstile widget when component is destroyed
	onDestroy(() => {
		if (browser && turnstileWidgetId && window.turnstile) {
			window.turnstile.remove(turnstileWidgetId);
		}
	});
</script>

<section class="displaySection">
	<section class="flex displaySection__row1">
		{#if $turnstileSetup === 'not-verified'}
			<div>
				<div class="cf-turnstile" bind:this={turnstileContainer}></div>
			</div>
		{:else if $turnstileSetup === 'verified'}
			{#each fileUploadFooterData as metric (metric.id)}
				<Metric
					iconName={metric.icon}
					heading={metric.heading}
					text={metric.text}
					color={metric.color}
				/>
			{/each}
		{/if}
	</section>
	<section class="flex displaySection__row2">
		<Metric iconName="Server" heading="Status" text={serverStatus} color="orange" animate />
	</section>
</section>

<style>
	.displaySection {
		display: grid;
		--spacing: 0.8rem;
		--internal-spacing: 0.4rem;
		gap: var(--spacing);
	}

	.displaySection__row1 {
		gap: var(--spacing);
	}

	.displaySection__row2 {
		justify-content: center;
	}
</style>
