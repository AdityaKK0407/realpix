<script lang="ts">
	import { BadgeAlert, Image } from 'lucide-svelte';
	import { onDestroy, onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { PUBLIC_TURNSTILE_SITE_KEY } from '$env/static/public';
	import { turnstile, type ErrorTurnstile } from '$lib/state/turnstile.svelte';

	interface Props {
		text: string[];
	}

	let props: Props = $props();
	let turnstileContainer: HTMLDivElement | null = null;
	let turnstileWidgetId: string | undefined = undefined;
	let errorTurnstile: ErrorTurnstile = $state({
		errorText: null,
		category: null,
		errorStatus: false
	});

	function handleTurnstileSuccess(token: string) {
		turnstile.changeTurnstileStatus({ status: 'verified', token });
	}

	function onTurnstileError(error: number) {
		turnstile.changeTurnstileStatus({ status: 'error', errorCode: error });
		errorTurnstile = turnstile.getErrorStatus();
	}

	function neededInteraction() {
		turnstile.changeTurnstileStatus({ status: 'manual-verification' });
	}

	onMount(() => {
		if (browser) {
			const checkTurnstile = setInterval(() => {
				if (window.turnstile && turnstileContainer && turnstile.shouldDisplay()) {
					clearInterval(checkTurnstile);
					turnstileWidgetId = window.turnstile.render(turnstileContainer, {
						sitekey: PUBLIC_TURNSTILE_SITE_KEY,
						callback: handleTurnstileSuccess,
						theme: 'light',
						size: 'normal',
						'error-callback': onTurnstileError,
						'before-interactive-callback': neededInteraction,
						'timeout-callback': () => {
							if(turnstileWidgetId) {
								turnstile.changeTurnstileStatus({status: 'verification-timeout', errorCode: 700000})
								errorTurnstile = turnstile.getErrorStatus();
								window.turnstile.reset(turnstileWidgetId);
							}
						},
						'expired-callback': () => {
							if (turnstileWidgetId) {
								turnstile.changeTurnstileStatus({ status: 'token-expired', errorCode: 710000})
								errorTurnstile = turnstile.getErrorStatus();
								window.turnstile.reset(turnstileWidgetId);
							}
						},
						retry: 'auto',
						"retry-interval": 10000
					});
					turnstile.changeTurnstileStatus({ status: 'verifying' });
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
		{#if errorTurnstile.errorStatus}
			<section class="row2__section">
				<BadgeAlert size="45" stroke="currentColor" />
				<section class="row2__section__text flex-column">
					<p class="md-font-1 flex section__text">
						<strong>Category: </strong> <span>{errorTurnstile.category}</span>
					</p>
					<p class="md-font-1 flex section__text">
						<strong>Message: </strong> <span>{errorTurnstile.errorText}</span>
					</p>
				</section>
			</section>
		{/if}
	</section>
</section>

<style>
	.mainSection {
		flex-grow: 1;
		display: grid;
		grid-template-rows: 1fr 0.3fr;
		grid-template-columns: 0.5fr 0.7fr 0.5fr;
		align-items: center;
		padding: var(--small-padding);
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
		align-items: center;
		gap: var(--text-gap);
		grid-column-start: 1;
		grid-column-end: 4;
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
	
	.row2__section__text {
		gap: var(--text-gap);
		align-items: center;
	}

	.section__text {
		gap: var(--text-gap);
	}

</style>
