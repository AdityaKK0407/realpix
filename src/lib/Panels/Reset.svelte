<script lang="ts">
	import { BadgeAlert, Image } from 'lucide-svelte';
	import { onDestroy, onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { PUBLIC_TURNSTILE_SITE_KEY } from '$env/static/public';
	import { turnstile } from '$lib/state/turnstile.svelte';

	interface Props {
		text: string[];
	}

	let props: Props = $props();
	let turnstileContainer: HTMLDivElement | null = null;
	let turnstileWidgetId: string | undefined = undefined;
	let errorText: string | null = $state(null);

	function handleTurnstileSuccess(token: string) {
		turnstile.changeTurnstileStatus('verified', token);
	}

	function onTurnstileError(error: Error) {
		turnstile.changeTurnstileStatus('error');
		errorText = error.message;
	}

	onMount(() => {
		if (browser && turnstile.getStatus() === 'not-verified') {
			const checkTurnstile = setInterval(() => {
				if (window.turnstile && turnstileContainer) {
					clearInterval(checkTurnstile);
					turnstileWidgetId = window.turnstile.render(turnstileContainer, {
						sitekey: PUBLIC_TURNSTILE_SITE_KEY,
						callback: handleTurnstileSuccess,
						theme: 'light',
						size: 'normal',
						'error-callback': onTurnstileError
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
	<section class="mainSection__row2 flex-column">
		<div class="cf-turnstile" bind:this={turnstileContainer}></div>
		{#if turnstile.getStatus() === 'error'}
			<section class="row2__section">
				<BadgeAlert size="35" stroke="currentColor" />
				<section class="row2__section__text">
					<p class="row2__strong sm-font-2">Error:</p>
					<p class="sm-font-3">{errorText}</p>
				</section>
			</section>
		{/if}
	</section>
</section>

<style>
	.mainSection {
		flex-grow: 1;
		display: grid;
		grid-template-rows: 0.7fr 0.3fr;
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

	.mainSection__row2 {
		grid-row-start: 2;
		grid-column-start: 2;
		align-items: center;
		gap: var(--text-gap);
	}

	.row2__section {
		display: flex;
		gap: var(--text-gap);
		align-items: center;
		color: var(--color-error);
		background-color: var(--color-error-lowest);
		padding: var(--medium-padding);
		border-radius: 2rem;
	}

	.row2__strong {
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.02em;
	}

	.row2__section__text {
		display: flex;
		gap: var(--text-gap-small);
		align-items: center;
	}
</style>
