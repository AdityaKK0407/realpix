<script lang="ts">
	interface Props {
		class?: string;
		size: number;
		ariaHidden?: boolean;
		ariaLabel?: string;
		strokeWidth?: number;
		fill?: string;
	}
	const props: Props = $props();
	const accessbilityLabels = $derived(
		props.ariaHidden
			? {
					'aria-hidden': true
				}
			: {
					role: 'img',
					'aria-label': props.ariaLabel,
					title: props.ariaLabel
				}
	);
</script>

<svg
	xmlns="http://www.w3.org/2000/svg"
	class={props.class}
	height={props.size}
	viewBox="0 -960 960 960"
	width={props.size}
	fill={props.fill}
	{...accessbilityLabels}
	stroke-width={props.strokeWidth}
	><path
		d="M240-320h480v-320H240v320Zm-80 160q-33 0-56.5-23.5T80-240v-480q0-33 23.5-56.5T160-800h640q33 0 56.5 23.5T880-720v480q0 33-23.5 56.5T800-160H160Zm0-80h640v-480H160v480Zm0 0v-480 480Zm160-160 85-113 55 73 75-100 105 140H320Z"
	/>
</svg>
