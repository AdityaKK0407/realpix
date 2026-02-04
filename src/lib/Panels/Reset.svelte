<script lang="ts">
	import { Info } from 'lucide-svelte';

	let props = $props();
</script>

<section>
	<Info size="45"/>
	<p class="md-font-2 bold">{props.text}</p>
</section>

<style>
    section {
        flex-grow: 1;
				display: flex;
				justify-content: center;
				align-items: center;
				gap: 1rem;
				color: var(--color-text-body);
    }
</style>