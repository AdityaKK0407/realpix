<script lang="ts">

	import { Check, Upload } from 'lucide-svelte';
	import { validateFiles } from '$lib/scripts/validatingFiles';

	let props = $props();

	let fileInput: HTMLInputElement;
	let button: HTMLButtonElement;
	let isOver: boolean = $state(false);
	let uploadSuccess: boolean = $state(false);
	let successText: string = $state('');
	let screenReaderMessage: string = $state('');
	let errorOccurred: boolean = $state(false);
	let firstText: string = $state('Click to Upload');
	let secondText: string = $state('or drag and drop');

	function handleFiles(files: FileList) {
		if (files.length > 0) {
			if (props.fileType == 'image') {
				const filesArray = Array.from(files);
				const filteredFilesArray = validateFiles(filesArray);
				if (filteredFilesArray.length > 0) {
					uploadSuccess = true;
					successText = `${files.length === 1 ? 'File' : 'Files'} uploaded successfully.`;
					screenReaderMessage = `${files.length === 1 ? 'One' : files.length} files have been selected successfully.`;
					button.blur();
					props.onSelect(Array.from(filteredFilesArray));
					if(errorOccurred) {
						errorOccurred = false;
					}
				} else {
					errorOccurred = true;
					firstText = 'An Error occurred.'
					secondText = 'Please upload a file with the correct extensions'
				}
			}
		}
	}

	function setOver(e: DragEvent, value: boolean) {
		e.preventDefault();
		isOver = value;
	}

	function keyBoardEvent(e: KeyboardEvent) {
		if (e.key === 'Enter' || e.key === ' ') {
			fileInput.click();
		}
	}

	function inputChange(e: Event) {
		const target = e.target as HTMLInputElement;
		if (target.files) {
			handleFiles(target.files);
		}
	}

	function drop(e: DragEvent) {
		if (e.dataTransfer) {
			e.preventDefault();
			isOver = false;
			handleFiles(e.dataTransfer.files);
		}
	}
</script>

<section class:error={errorOccurred}>
	<button
		bind:this={button}
		class='dropzone'
		class:drop-area={!errorOccurred}
		class:dropping={isOver}
		class:neutral={!isOver}
		class:success={uploadSuccess}
		class:error={errorOccurred}
		ondragover={(e) => setOver(e, true)}
		ondragleave={(e) => setOver(e, false)}
		ondrop={drop}
		onkeydown={keyBoardEvent}
		onclick={() => {
			if(!isOver && !uploadSuccess) {
				fileInput.click()
			}}}
		aria-label="Drag and drop images area"
	>
		<input
			type="file"
			class="hidden"
			bind:this={fileInput}
			onchange={inputChange}
			accept="image/*"
			multiple
		/>

		{#if !isOver && !uploadSuccess}
			<section class="dropzone-text">
				<strong class="lg-font-2">{firstText}</strong>
				<p class="md-font-1">{secondText}</p>
			</section>
			<small class="sm-font-1">{props.extensions}</small>

		{:else if uploadSuccess }
			<section>
				<p class="sr-only" aria-live="polite">{screenReaderMessage}</p>
				<Check size="40" aria-hidden="true" />
				<p class="md-font-2 bold" aria-hidden="true">{successText}</p>
			</section>

		{:else }
			<section class="drop-field">
				<Upload size="25" />
				<p class="md-font-2 bold">Drop the file</p>
			</section>
		{/if}

	</button>
</section>

<style>
    section {
        width: 100%;
    }

    .drop-area {
        border-width: 0.25rem;
        border-color: var(--color-border-neutral);
    }

    .dropzone {
        display: flex;
        flex-direction: column;
        gap: 0.9rem;
        justify-content: center;
        padding-inline: var(--file-upload-padding-inline);
        padding-block: var(--file-upload-padding-block);
        border-radius: 0.6rem;
        height: 15rem;
    }

    .dropzone-text {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .neutral {
        border-style: dashed;
    }

    .dropping {
        background-color: var(--color-bg-dragover);
        border-color: var(--color-border-dragover);
        border-style: solid;
        cursor: default;
    }

    .drop-field {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: var(--text-gap);
    }

    button {
        width: 100%;
        background-color: var(--color-bg-neutral);
    }

    .success {
        border-color: var(--color-border-success);
        background-color: var(--color-bg-success);
        color: var(--color-text-success);
        pointer-events: none;
    }

		.error {
				border-color: var(--color-border-error);
				background-color: var(--color-bg-error);
				color: var(--color-text-error);
		}
</style>