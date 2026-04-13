import { PUBLIC_BASE_TIME_REQUEST, PUBLIC_REQUEST_BIAS } from '$env/static/public';
// import type { UUID } from 'crypto';

export interface Task_ID {
	task_id: string;
	idOfBatchs: string[] | undefined;
	interval: number;
	pingCount: number;
	taskStatus: 'completed' | 'timeout' | 'pending';
	taskResolve: ((value: string | PromiseLike<string>) => void) | null;
}

export interface InputTask_ID {
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
	private schedulerQueue: string[];

	constructor() {
		this.task_ids = $state([]);
		this.base_time = 0;
		this.threshold_pings = 0;
		this.increase_time_value = 0;
		this.pingCount = 0;
		this.threshold_reached = false;
		this.task_time = [];
		this.length = 0;
		this.schedulerQueue = [];
	}

	private getTaskInfo(task_id: string) {
		return this.task_ids.filter((task) => task.task_id === task_id)[0];
	}

	private taskScheduler() {
		if (this.schedulerQueue.length === 0) return;

		const task_id = this.schedulerQueue.pop();
		if (!task_id) return;

		const task = this.getTaskInfo(task_id);
		setTimeout(async () => {
			const response = await fetch('/api/modelStatus', {
				method: 'POST',
				body: JSON.stringify({
					task_id: task.task_id
				})
			});

			const responseData = await response.json();
			switch (response.status) {
				case 200:
					if (responseData.status !== 'completed') {
						this.schedulerQueue.push(task_id);
						this.taskScheduler();
					} else {
						// for task ping success
					}
					break;

				case 429:
					this.schedulerQueue.push(task_id);
					alert('Rate limiting exceeded. Showing turnstile');
					break;

				case 500:
				default:
					this.taskScheduler();
			}
		}, task.interval);
	}

	addTasks(tasks: InputTask_ID): void {
		if (tasks.idOfBatchs) {
			const taskToAdd: Task_ID = {
				...tasks,
				interval: tasks.idOfBatchs?.length * this.base_request_time * this.request_bias,
				taskStatus: 'pending',
				pingCount: 0,
				taskResolve: null
			};
			this.schedulerQueue.push(taskToAdd.task_id);

			new Promise((resolve) => {
				taskToAdd.taskResolve = resolve;
			});

			const tasksArray: Task_ID[] = [...this.task_ids, taskToAdd];
			this.task_ids = tasksArray;
		}
	}

	startPinging() {
		this.taskScheduler();
	}
}

const processingStatus = new TaskPinging();

export { processingStatus };
