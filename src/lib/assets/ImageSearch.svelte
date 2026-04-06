<script lang="ts">
	interface Props {
		class?: string;
		size: number;
		ariaHidden?: boolean;
		ariaLabel?: string;
		strokeWidth?: number;
		fill?: string;
		stroke?: string;
		backgroundStroke?: string;
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
	width={props.size}
	height={props.size}
	viewBox="0 0 661 703"
	xmlns="http://www.w3.org/2000/svg"
	fill="none"
	stroke={props.stroke}
	stroke-linecap="round"
	stroke-linejoin="round"
	version="1.1"
	stroke-opacity="1"
	{...accessbilityLabels}
	class={props.class}
	stroke-width={props.strokeWidth}
>
	<!-- Image frame -->
	<path
		d="M48,128C48,101.508056640625,69.508056640625,80,96,80L416,80C442.491943359375,80,464,102.508056640625,464,129L464,384C464,410.491943359375,442.491943359375,432,416,432L96,432C69.508056640625,432,48,410.491943359375,48,384L48,128"
	/>

	<!-- Mountain / image preview lines -->
	<path
		d="M48,352L48,384C48,410.491943359375,69.508056640625,432,96,432L416,432C442.491943359375,432,464,410.491943359375,464,384L464,368L390.45001220703125,306.659912109375C377.72491455078125,296.07861328125,359.03076171383,296.94580078125,347.34002685546875,308.659912109375L304,335.7900390625L213.34002685546875,245.300048828125C201.3642578125,233.326904296875,182.13372802734375,232.757080078125,169.47003173828125,244L48,352Z"
	/>

	<!-- Sun dot -->
	<ellipse cx="211" cy="148" rx="32" ry="32" stroke-miterlimit="10" fill={props.fill} />

	<!-- Outer search circle -->
	<ellipse
		cx="369"
		cy="406.0000000000002"
		rx="195"
		ry="198.00000000000023"
		stroke={props.backgroundStroke}
		stroke-width="35"
	/>

	<!-- Search circle outline -->
	<path
		d="M361.567138671875,245.375C272.2672119140625,245.37548828125,199.87493896484375,317.217529296875,199.87493896484375,405.83984375C199.875,494.46240234375,272.26702880859375,566.3046875,361.56719970703125,566.304931640625C450.86724853515625,566.305419921875,523.259521484375,494.46240234375,523.2594604492188,405.840087890625C523.2538452148438,317.22021484375,450.86505126953125,245.380859375,361.567138671875,245.375Z"
		stroke-miterlimit="5"
		stroke-width="47"
	/>

	<!-- Search handle line -->
	<path d="M482.2008056640625,525.55859375L595.125,637.624755859375" stroke-miterlimit="10" />

	<!-- Inner search circle (on top) -->
	<ellipse
		cx="362"
		cy="404.9999999999998"
		rx="150.5"
		ry="143.99999999999977"
		stroke-width="28"
		stroke={props.backgroundStroke}
	/>
</svg>
