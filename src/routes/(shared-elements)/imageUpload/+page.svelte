<script lang="ts">
	import FileUpload from '$lib/Components/FileUpload.svelte';
	import { type FileType, uploadData } from '$lib/state/uploadFlow.svelte';
	import { mainState } from '$lib/upload/upload.svelte';
	import Reset from '$lib/Panels/Reset.svelte';
	import ReadyPanel from '$lib/Panels/ReadyPanel.svelte';
	import { Panel } from '$lib/types/Panel';
	import Processing from '$lib/Panels/Processing.svelte';
	import { type SeoConfig, Head } from 'svead';
	import { PUBLIC_WEBSITE_URL } from '$env/static/public';

	function setFiles(newFiles: File[], fileType: FileType) {
		uploadData.uploadFiles(newFiles, fileType);
		mainState.transitionState('SELECT_IMAGE');
		activePanel = Panel.Processing_Panel;
	}

	function setClassNames(panelNo: Panel) {
		return activePanel === panelNo ? 'active-layout' : 'inactive-layout';
	}

	let activePanel: Panel = $state(Panel.Uploading_Panel);
	const uploadFlow = $derived(mainState.getUploadState());

	const seo_config: SeoConfig = {
		title: 'Detect AI Images - RealPix Deepfake Detection System',
		description:
			'Upload any image to detect if it was AI generated and verify authenticity. RealPix gives a confidence score for the uploaded images.',
		url: `${PUBLIC_WEBSITE_URL}/imageUpload`,
		website: PUBLIC_WEBSITE_URL,
		author_name: 'Team Fabulous',
		site_name: 'RealPix'
	};
</script>

<Head {seo_config} />
<main>
	<section class={setClassNames(Panel.Uploading_Panel)} class:items-center={true}>
		<FileUpload onSelect={setFiles} extensions="PNG, JPG, JPEG" fileType="image" />
	</section>
	<section class={setClassNames(Panel.Processing_Panel)} class:relative={true}>
		{#if uploadFlow === 'idle'}
			<Reset text={['Upload images to begin analyzing', 'for authenticity']} />
		{:else if uploadFlow === 'ready'}
			<ReadyPanel fileType="image" />
		{:else if uploadFlow === 'processing'}
			<Processing fileType="image" />
		{/if}
	</section>
</main>

<style>
	main {
		display: grid;
		grid-template-columns: 0.32fr 0.68fr;
		gap: var(--layout-panel-gap);
		transition: grid-template-columns 500ms ease-in-out;
	}

	section {
		background-color: var(--color-bg-surface);
		border-radius: var(--layout-panel-rounded);
		padding-inline: var(--app-padding-inline);
		padding-block: var(--app-padding-block);
		transition: filter 400ms ease-in-out;
		display: flex;
	}
</style>
