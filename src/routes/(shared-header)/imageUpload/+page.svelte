<script lang="ts">
	import FileUpload from '$lib/Components/FileUpload.svelte';
	import { type FileType, uploadData } from '$lib/state/uploadFlow.store';
	import { transition, uploadState } from '$lib/upload/upload.store';
	import Reset from '$lib/Panels/Reset.svelte';
	import ReadyPanel from '$lib/Panels/ReadyPanel.svelte';
	import { Panel } from '$lib/types/Panel';
	import UploadingPanel from '$lib/Panels/UploadingPanel.svelte';
	import ProgressBar from '$lib/Components/ProgressBar.svelte';

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

<main class:reduce-grid={activePanel === Panel.Processing_Panel}>
	<ProgressBar />
	<section
		class={setClassNames(Panel.Uploading_Panel)}
		class:items-center={true}
		class:panel__1={true}
	>
		<FileUpload onSelect={setFiles} extensions="PNG, JPG, JPEG" fileType="image" />
	</section>
	<section class={setClassNames(Panel.Processing_Panel)} class:panel__2={true}>
		{#if $uploadState === 'idle'}
			<Reset
				text={[
					'AI Model is ready to complete your request.',
					'Please select an image to get started'
				]}
				serverStatus={true}
				inactiveText={[
					'Please wait for the AI Model to be activated.',
					'We are sorry for the inconvenience caused.'
				]}
			/>
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
		grid-template-columns: 0.3fr 0.7fr;
		grid-template-rows: 0.085fr 1fr;
		gap: var(--layout-panel-gap);
		transition: grid-template-columns 500ms ease-in-out;
	}

	.reduce-grid {
		grid-template-columns: 0.26fr 0.84fr;
	}

	section {
		background-color: var(--color-bg-surface);
		border-radius: var(--layout-panel-rounded);
		padding-inline: var(--app-padding-inline);
		padding-block: var(--app-padding-block);
		transition: filter 400ms ease-in-out;
		display: flex;
	}

	.panel__1 {
		grid-row-start: 2;
		grid-column-start: 1;
	}

	.panel__2 {
		grid-row-start: 2;
		grid-column-start: 2;
	}
</style>
