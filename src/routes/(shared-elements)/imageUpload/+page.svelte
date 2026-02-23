<script lang="ts">
	import FileUpload from '$lib/Components/FileUpload.svelte';
	import { type FileType, uploadData } from '$lib/state/uploadFlow.store';
	import { transition, uploadState } from '$lib/upload/upload.store';
	import Reset from '$lib/Panels/Reset.svelte';
	import ReadyPanel from '$lib/Panels/ReadyPanel.svelte';
	import { Panel } from '$lib/types/Panel';
	import UploadingPanel from '$lib/Panels/UploadingPanel.svelte';

	function setFiles(newFiles: File[], fileType: FileType) {
		uploadData.uploadFiles(newFiles, fileType);
		transition('SELECT_IMAGE');
		activePanel = Panel.Processing_Panel;
	}

	function setClassNames(panelNo: Panel) {
		return activePanel === panelNo ? 'active-layout' : 'inactive-layout';
	}

	let activePanel: Panel = $state(Panel.Uploading_Panel);
</script>

<svelte:head>
	<title>Image Upload</title>
</svelte:head>

<main>
	<section class={setClassNames(Panel.Uploading_Panel)} class:items-center={true}>
		<FileUpload onSelect={setFiles} extensions="PNG, JPG, JPEG" fileType="image" />
	</section>
	<section class={setClassNames(Panel.Processing_Panel)}>
		{#if $uploadState === 'idle'}
			<Reset text={['Upload images to begin analyzing', 'for authenticity']} />
		{:else if $uploadState === 'ready'}
			<ReadyPanel fileType="image" />
		{:else if $uploadState === 'uploading'}
			<UploadingPanel fileType="image" />
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
