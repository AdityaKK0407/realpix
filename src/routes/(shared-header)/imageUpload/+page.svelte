<script lang="ts">
	import FileUpload from '$lib/Components/FileUpload.svelte';
	import { type FileUploader, uploadedFiles } from '$lib/state/uploadFlow.store';
	import { transition, uploadState } from '$lib/upload/upload.store';
	import Reset from '$lib/Panels/Reset.svelte';
	import ReadyPanel from '$lib/Panels/ReadyPanel.svelte';
	import { nanoid } from 'nanoid';
	import { Panel } from '$lib/types/Panel';

	function setFiles(newFiles: File[], fileType: 'image' | 'video') {
		const newItems: FileUploader[] = newFiles.map((file: File) => {
			return {
				id: nanoid(),
				type: fileType,
				src: file
			};
		});
		uploadedFiles.update((file) => [...file, ...newItems]);
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
	<section class={setClassNames(Panel.Uploading_Panel)} class:items-center={true}>
		<FileUpload onSelect={setFiles} extensions="PNG, JPG, JPEG" fileType="image" />
	</section>
	<section class={setClassNames(Panel.Processing_Panel)}>
		{#if $uploadState === 'idle'}
			<Reset text="Select images to start the process" />
		{:else if $uploadState === 'ready'}
			<ReadyPanel fileType="image" />
		{/if}
	</section>
</main>

<style>
	main {
		display: grid;
		grid-template-columns: 0.3fr 0.7fr;
		gap: var(--layout-panel-gap);
		transition: grid-template-columns 500ms ease-in-out;
	}

	.reduce-grid {
		grid-template-columns: 0.27fr 0.83fr;
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
