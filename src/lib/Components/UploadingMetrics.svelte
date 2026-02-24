<script lang="ts">
	import {fileUploadFooterData} from '$lib/data/FileUploadingMetrics.data';

	import {type ServerStatus} from '$lib/types/fileupload.types';
	import Metric from './Metric.svelte';

	let serverStatus: ServerStatus = $state('InActive');
</script>

<section class="displaySection">
    <section class="flex displaySection__row1">
        {#each fileUploadFooterData as metric (metric.id)}
            <Metric
                    iconName={metric.icon}
                    heading={metric.heading}
                    text={metric.text}
                    color={metric.color}
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
