export interface ICluster {
  uuid: string;
  name: string;
  workersQuantity: number;
  instanceType: string;
  status: string;
  bodoVersion: string;
  nodesIp: string[];
}

export interface IConfig {
  allowLocalExecution: any;
  e: any;
  auto_attach: any;
  catalog_mode: any;
}

// Should be kept in sync with https://github.com/Bodo-inc/bodo-platform-ipyparallel-kernel/blob/009b46f6b654a3ca38cbc29030c84601b044ee1d/bodo_platform_ipyparallel_kernel/kernel.py#L30
export enum SupportedLanguages {
  PARALLEL_PYTHON = 'Parallel-Python',
  PYTHON = 'Python',
  SQL = 'SQL',
}
