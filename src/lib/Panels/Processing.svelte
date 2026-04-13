<script lang="ts">
	import { processingStatus, type InputTask_ID } from '$lib/state/processingResult.svelte';
	import { type FileType, uploadData, type UploadType } from '$lib/state/uploadFlow.svelte';

	interface Props {
		fileType: FileType;
	}

	const props: Props = $props();

	async function uploadBatch(batch: UploadType): Promise<void> {
		try {
			if (batch && batch.formData && batch.batchId) {
				const batchResponse = await fetch('/api/uploadImage', {
					method: 'POST',
					body: batch.formData
				});

				if (!batchResponse.ok) {
					alert(batchResponse.statusText);
					return;
				} else {
					const batchResponseData = await batchResponse.json();
					const processingData: InputTask_ID = {
						task_id: batchResponseData.data.task_ids,
						idOfBatchs: batch.batchId
					};
					processingStatus.addTasks(processingData);
				}
			}
		} catch (err) {
			alert(err);
		}
	}

	async function upload() {
		const packages = uploadData.createPackages(props.fileType);
		if (packages) {
			const { sendData } = packages;
			let successTransaction = true;

			const actions = sendData.map(uploadBatch);

			await Promise.all(actions);
			if (packages.moreBatchAvailable) {
				alert('More packages available');
			}

			if (successTransaction) {
				processingStatus.startPinging();
			}
		}
	}

	upload();
</script>

<section class="uploading__container">
	<p>Uploaded</p>
</section>

<style>
	.uploading__container {
		flex-grow: 1;
	}
</style>
