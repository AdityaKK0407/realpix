<script lang="ts">
	import { Info } from 'lucide-svelte';
	import { resolve } from '$app/paths';
	import { fileUploadFooterData } from '$lib/data/FileUploadingMetrics.data';
	import Metric from '$lib/Components/Metric.svelte';
	import { turnstile } from '$lib/state/turnstile.svelte';
</script>

<svelte:head>
	<script
		src="https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit"
		async
		defer
	></script>
	<link rel="canonical" href="https://fab-realpix.netlify.app" />
</svelte:head>

<section class="pageContainer">
	<header class="pageContainer__header">
		<section>
			<a href={resolve('/')} class="pageContainer__header__link">RealPix</a>
		</section>
		<section class="pageContainer__header__col2">
			<section class="displaySection">
				<section class="flex displaySection__row1">
					{#each fileUploadFooterData as metric (metric.id)}
						<Metric
							iconName={metric.icon}
							heading={metric.heading}
							text={metric.iconType.includes('security') ? turnstile.getStatusInfo() : metric.text}
							iconType={metric.iconType}
						/>
					{/each}
				</section>
			</section>
		</section>
	</header>
	<slot />
	<footer class="pageContainer__footer">
		<Info size="27" stroke="currentColor" />
		<p class="sm-font-2 pageContainerFooter__text">
			<strong>Note: </strong>
			File(s) are deleted after processing.
		</p>
	</footer>
</section>

<style>
	.pageContainer {
		display: grid;
		grid-template-rows: 0.13fr 1fr 0.08fr;
		height: 100dvh;
		background-color: var(--color-bg-app);
		padding-inline: var(--app-padding-inline);
		padding-block: var(--app-padding-block);
		gap: var(--text-gap-small);
	}

	.pageContainer__header {
		display: grid;
		grid-template-columns: 0.2fr 1fr 0.2fr;
	}

	.pageContainer__header__link {
		text-decoration: none;
	}

	.pageContainer__header__col2 {
		justify-self: center;
	}

	.displaySection {
		display: grid;
		--spacing: 0.8rem;
		--internal-spacing: 0.4rem;
		gap: var(--spacing);
	}

	.displaySection__row1 {
		gap: var(--spacing);
	}

	.pageContainer__footer {
		display: flex;
		gap: var(--text-gap);
		justify-content: center;
		align-items: center;
		color: var(--color-primary);
		background-color: var(--color-warm-gray);
		padding: var(--small-padding);
		border-radius: 0.8rem;
	}

	.pageContainerFooter__text {
		color: var(--color-text-body);
	}
</style>
