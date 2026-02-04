<script lang="ts">
	import FileUpload from '$lib/Components/FileUpload.svelte';
	import { uploadedFiles } from './stores/uploadFlow.store';
	import { transition, uploadState } from '$lib/upload/upload.store';
	import Reset from '$lib/Panels/Reset.svelte';
	import ReadyPanel from '$lib/Panels/ReadyPanel.svelte';

	function setFiles(newFiles: File[]) {
		uploadedFiles.update(files => [...files, ...newFiles]);
		transition('SELECT_IMAGE');
		activePanel = 2;
	}

	function setClassNames(panelNo: 1 | 2) {
		return activePanel === panelNo ? 'active-layout' : 'inactive-layout';
	}

	let activePanel: 1 | 2 = $state(1);
</script>

<svelte:head>
	<title>Image Upload</title>
</svelte:head>

<main>
	<section class={setClassNames(1)} class:items-center={true}>
		<FileUpload onSelect={setFiles} extensions="PNG, JPG, JPEG or WEBP" fileType="image" />
	</section>
	<section class={setClassNames(2)}>
		{#if $uploadState === 'idle'}
			<Reset text="Select images to start the process" />
		{:else if $uploadState === 'ready'}
			<ReadyPanel />
		{/if}
	</section>
</main>

<style>
    main {
        display: grid;
        grid-template-columns: 0.26fr 0.74fr;
        gap: var(--layout-panel-gap);
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