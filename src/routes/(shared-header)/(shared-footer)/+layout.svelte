<script lang="ts">
	import { Info } from 'lucide-svelte';
</script>

<slot />
<footer>
	<Info size="24" stroke="currentColor" />
	<p class="sm-font-3">
		<strong>Note: </strong>
		File(s) are deleted after processing.
	</p>
</footer>

<style>
	footer {
		display: flex;
		gap: var(--text-gap);
		justify-content: center;
		align-items: center;
		color: var(--color-primary-900);
	}
</style>
