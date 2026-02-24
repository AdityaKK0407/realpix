<script lang="ts">
	import { fileUploadFooterData } from '$lib/data/FileUploadingMetrics.data';

	import Metric from './Metric.svelte';
</script>

<section class="displaySection">
	<section class="flex displaySection__row1">
		{#each fileUploadFooterData as metric (metric.id)}
			<Metric
				iconName={metric.icon}
				heading={metric.heading}
				text={metric.text}
				color={metric.color}
				turnstileSupport={metric.turnstileSupport}
			/>
		{/each}
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
</style>
