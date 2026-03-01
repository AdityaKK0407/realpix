<script lang="ts">
	import { CircleX, Info, TriangleAlert } from 'lucide-svelte';

	interface Props {
		alertType: 'info' | 'warning' | 'critical';
        heading: string;
        body: string
	}
	const props: Props = $props();
</script>

<section>
	<div>
		{#if props.alertType === 'info'}
			<Info />
		{:else if props.alertType === 'warning'}
			<TriangleAlert />
		{:else if props.alertType === 'critical'}
			<span class="material-symbols-outlined"> dangerous </span>
		{/if}
	</div>
    <section>
        <h3>{props.heading}</h3>
        <p>{props.body}</p>
    </section>
    <div>
        <CircleX />
    </div>
</section>
