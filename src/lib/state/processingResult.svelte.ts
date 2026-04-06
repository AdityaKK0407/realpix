import { PUBLIC_BASE_TIME_REQUEST, PUBLIC_REQUEST_BIAS } from '$env/static/public';
// import type { UUID } from 'crypto';

export interface Task_ID {
	task_id: string;
	idOfBatchs: string[] | undefined;
}

class TaskPinging {
	private task_ids: Task_ID[];
	private base_time: number;
	private threshold_pings: number;
	private pingCount: number;
	private increase_time_value: number;
	private base_request_time = parseInt(PUBLIC_BASE_TIME_REQUEST);
	private request_bias = parseInt(PUBLIC_REQUEST_BIAS);
	private threshold_reached: boolean;
	private task_time: number[];
	private length: number;

	constructor() {
		this.task_ids = $state([]);
		this.base_time = 0;
		this.threshold_pings = 0;
		this.increase_time_value = 0;
		this.pingCount = 0;
		this.threshold_reached = false;
		this.task_time = [];
		this.length = 0;
	}

	addTasks(tasks: Task_ID): void {
		const tasksArray: Task_ID[] = [...this.task_ids, tasks];
		this.task_ids = tasksArray;
	}

	private noOfTasksPerTask(index: number) {
		const value = this.task_ids[index];
		return value.idOfBatchs?.length;
	}

	private determineThresholdPings() {
		switch (this.length) {
			case 1:
			case 2:
			case 3:
				this.threshold_pings = this.length;
				break;

			case 4:
			case 5:
				this.threshold_pings = this.length - 1;
				break;

			default:
				this.threshold_pings = 5;
		}
	}

	private determineTimeLimit() {
		this.length = this.task_ids.length;
		for (let len = 0; len < this.length; len++) {
			const taskLen = this.noOfTasksPerTask(len);
			if (taskLen) {
				this.task_time.push(this.base_request_time * taskLen + this.request_bias);
			}
		}
		this.determineThresholdPings();
	}

	startPinging() {
		this.determineTimeLimit();

		const request1 = setInterval(() => {
			if (this.pingCount > this.threshold_pings) {
				clearInterval(request1);
				this.threshold_reached = true;
			} else {
				this.task_ids.forEach(async (task) => {
					const response = await fetch('/api/modelStatus', {
						method: 'POST',
						body: JSON.stringify({ task_id: task.task_id })
					});
				});
				this.pingCount++;
			}
		}, this.base_time);
	}
}

const processingStatus = new TaskPinging();

export { processingStatus };
