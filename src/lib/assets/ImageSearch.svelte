<script lang="ts">
	interface Props {
		class?: string;
		size: number;
		ariaHidden?: boolean;
		ariaLabel?: string;
		strokeWidth?: number;
		fill?: string;
		stroke?: string;
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
	class={props.class}
	width={props.size}
	xmlns="http://www.w3.org/2000/svg"
	height={props.size}
	viewBox="0 0 661 703"
	fill={props.fill}
	stroke={props.stroke}
	stroke-width={props.strokeWidth}
	version="1.1"
	{...accessbilityLabels}
>
	<g id="shape-35802bb9-e4b3-80d6-8007-c0549d1baa39" rx="0" ry="0">
		<g rx="0" ry="0">
			<g>
				<g>
					<path
						d="M48,128C48,101.508057,69.508057,80,96,80L416,80C442.491943,80,464,102.508057,464,129L464,384C464,410.491943,442.491943,432,416,432L96,432C69.508057,432,48,410.491943,48,384L48,128"
						stroke-linejoin="round"
					>
					</path>
				</g>
				<g stroke-linejoin="round">
					<g class="stroke-shape">
						<path
							d="M48,128C48,101.508057,69.508057,80,96,80L416,80C442.491943,80,464,102.508057,464,129L464,384C464,410.491943,442.491943,432,416,432L96,432C69.508057,432,48,410.491943,48,384L48,128"
						>
						</path>
					</g>
				</g>
			</g>
			<g id="shape-35802bb9-e4b3-80d6-8007-c0509c861e87">
				<g class="fills" id="fills-35802bb9-e4b3-80d6-8007-c0509c861e87">
					<path
						d="M304,335.790039L213.340027,245.300049C201.364258,233.326904,182.133728,232.75708,169.470032,244L48,352M224,432L347.340027,308.659912C359.030762,296.945801,377.724915,296.078613,390.450012,306.659912L464,368"
						stroke-linecap="round"
						stroke-linejoin="round"
					>
					</path>
				</g>
				<g stroke-linecap="round" stroke-linejoin="round">
					<g class="stroke-shape">
						<path
							d="M304,335.790039L213.340027,245.300049C201.364258,233.326904,182.133728,232.75708,169.470032,244L48,352M224,432L347.340027,308.659912C359.030762,296.945801,377.724915,296.078613,390.450012,306.659912L464,368"
							stroke-width={props.strokeWidth}
						>
						</path>
					</g>
				</g>
			</g>
			<g id="shape-35802bb9-e4b3-80d6-8007-c0509c8592b8">
				<g class="fills" id="fills-35802bb9-e4b3-80d6-8007-c0509c8592b8">
					<ellipse
						cx="211"
						cy="148"
						rx="32"
						ry="32"
						transform="matrix(1.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000)"
						stroke-miterlimit="10"
						stroke="#fafafa"
					>
					</ellipse>
				</g>
				<g stroke-miterlimit="10">
					<g class="stroke-shape">
						<ellipse
							cx="211"
							cy="148"
							rx="32"
							ry="32"
							transform="matrix(1.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000)"
							stroke="#fafafa"
						>
						</ellipse>
					</g>
				</g>
			</g>
			<g id="shape-35802bb9-e4b3-80d6-8007-c0509c835c33" style="display:none">
				<g>
					<rect
						rx="0"
						ry="0"
						x="0"
						y="0"
						transform="matrix(1.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000)"
						width="512.0000000000002"
						height="512"
					>
					</rect>
				</g>
			</g>
		</g>
		<g>
			<g>
				<ellipse
					cx="361.5"
					cy="406"
					rx="196.5"
					ry="198.00000000000023"
					transform="matrix(1.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000)"
				>
				</ellipse>
			</g>
			<g>
				<g transform="matrix(1.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000)">
					<defs>
						<ellipse cx="361.5" cy="406" rx="196.5" ry="198.00000000000023"> </ellipse>
					</defs>
				</g>
			</g>
		</g>
		<g
			id="shape-35802bb9-e4b3-80d6-8007-c0509c3789b6"
			style="fill:#000000"
			class="ionicon"
			rx="0"
			ry="0"
		>
			<g id="shape-35802bb9-e4b3-80d6-8007-c0509c3d3f8e" style="display:none">
				<g class="fills" id="fills-35802bb9-e4b3-80d6-8007-c0509c3d3f8e">
					<rect
						rx="0"
						ry="0"
						x="134"
						y="180"
						transform="matrix(1.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000)"
						width="527.0000000000001"
						height="523.0000000000014"
						fill={props.fill}
					>
					</rect>
				</g>
			</g>
			<g>
				<g>
					<path
						d="M361.567139,245.375C272.267212,245.375488,199.874939,317.217529,199.874939,405.839844C199.875,494.462402,272.267029,566.304688,361.5672,566.304932C450.867249,566.30542,523.259521,494.462402,523.25946,405.840088C523.253845,317.220215,450.865051,245.380859,361.567139,245.375Z"
						stroke-miterlimit="10"
					>
					</path>
				</g>
				<g stroke-miterlimit="10">
					<g class="stroke-shape">
						<path
							d="M361.567139,245.375C272.267212,245.375488,199.874939,317.217529,199.874939,405.839844C199.875,494.462402,272.267029,566.304688,361.5672,566.304932C450.867249,566.30542,523.259521,494.462402,523.25946,405.840088C523.253845,317.220215,450.865051,245.380859,361.567139,245.375Z"
						>
						</path>
					</g>
				</g>
			</g>
			<g>
				<g>
					<path
						d="M482.200806,525.558594L595.125,637.624756"
						stroke-linecap="round"
						stroke-miterlimit="10"
					>
					</path>
				</g>
				<g stroke-linecap="round" stroke-miterlimit="10">
					<g class="stroke-shape">
						<path d="M482.200806,525.558594L595.125,637.624756"> </path>
					</g>
				</g>
			</g>
		</g>
		<g>
			<g>
				<ellipse
					cx="-725.5"
					cy="2755"
					rx="150.5"
					ry="143.99999999999977"
					transform="matrix(1.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000)"
				>
				</ellipse>
			</g>
			<g>
				<g transform="matrix(1.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000)">
					<defs>
						<ellipse
							cx="-725.5"
							cy="2755"
							rx="150.5"
							ry="143.99999999999977"
							fill={props.fill}
							stroke-width={props.strokeWidth}
							id="stroke-shape-render-322-35802bb9-e4b3-80d6-8007-c05411c35d2f-0"
						>
						</ellipse>
					</defs>
				</g>
			</g>
		</g>
	</g>
</svg>
