import { PUBLIC_BASE_TIME_REQUEST, PUBLIC_REQUEST_BIAS } from '$env/static/public';

class TaskPinging {
	private task_ids: string[];
	private base_time: number;
	private threshold_pings: number;
	private pingCount: number;
	private increase_time_value: number;
	private base_request_time = parseInt(PUBLIC_BASE_TIME_REQUEST);
	private request_bias = parseInt(PUBLIC_REQUEST_BIAS);
	private threshold_reached: boolean;

	constructor() {
		this.task_ids = $state([]);
		this.base_time = 0;
		this.threshold_pings = 0;
		this.increase_time_value = 0;
		this.pingCount = 0;
		this.threshold_reached = false;
	}

	addTasks(tasks: string[]): void {
		const tasksArray = [...this.task_ids, ...tasks];
		this.task_ids = tasksArray;
	}

	private determineTimeLimit() {
		const length = this.task_ids.length;
		this.base_time = this.base_request_time * length + this.request_bias;
		switch (length) {
			case 1:
			case 2:
				this.threshold_pings = length;
				this.increase_time_value = this.base_request_time / length;
				break;

			case 3:
			case 4:
			case 5:
				this.threshold_pings = length - 1;
				this.increase_time_value = Math.floor((this.base_request_time / length) * 1.2);
				break;

			default:
				alert('Some error occurred.');
		}
	}

	startPinging() {
		this.determineTimeLimit();
		console.log('hi started pining');

		const request1 = setInterval(() => {
			if (this.pingCount > this.threshold_pings) {
				clearInterval(request1);
				this.threshold_reached = true;
			} else {
				this.task_ids.forEach(async (task) => {
					const response = await fetch('/api/modelStatus', {
						method: 'POST',
						body: JSON.stringify({ task_id: task })
					});
				});
				this.pingCount++;
			}
		}, this.base_time);
	}
}

const processingStatus = new TaskPinging();

export { processingStatus };
