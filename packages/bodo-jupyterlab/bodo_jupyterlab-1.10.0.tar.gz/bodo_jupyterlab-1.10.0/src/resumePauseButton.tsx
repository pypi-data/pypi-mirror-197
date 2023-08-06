import React, { SyntheticEvent } from 'react';
import { Grid } from 'react-loader-spinner';
import { pauseClusterHandler, resumeClusterHandler } from './handler';

type Props = {
  clusterStatus: string;
  uuid: string;
  startLoading: (status: string) => void;
  loading: boolean;
  forceUpdate: () => void;
};

const ClusterResumePause = ({ clusterStatus, uuid, startLoading, loading, forceUpdate }: Props) => {
  const pauseCluster = (cluster_uuid: string) => async (e: SyntheticEvent) => {
    if (
      !confirm(
        'Are you sure that you want to pause this cluster? Make sure not to pause clusters while the kernel is connecting.'
      )
    ) {
      return false;
    }
    await pauseClusterHandler(cluster_uuid);
    startLoading('PAUSING');
    forceUpdate();
  };

  const resumeCluster = (cluster_uuid: string) => async (e: SyntheticEvent) => {
    if (!confirm('Are you sure that you want to resume this cluster')) {
      return false;
    }
    await resumeClusterHandler(cluster_uuid);
    startLoading('RESUMING');
    forceUpdate();
  };

  if (!(clusterStatus === 'RUNNING' || clusterStatus === 'PAUSED') || loading) {
    return (
      <span>
        <Grid ariaLabel="loading-indicator" width={10} height={10} />
      </span>
    );
  }

  return (
    <div
      className="bodo-cluster-list-pause-unpause"
      onClick={clusterStatus === 'RUNNING' ? pauseCluster(uuid) : resumeCluster(uuid)}
    >
      {clusterStatus === 'RUNNING' ? (
        <svg
          width="31"
          height="46"
          viewBox="0 0 31 46"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            fill-rule="evenodd"
            clip-rule="evenodd"
            d="M5 0C7.76143 0 10 2.23858 10 5L10 41C10 43.7614 7.76142 46 5 46C2.23858 46 0 43.7614 0 41L1.43051e-06 5C1.90735e-06 2.23858 2.23858 0 5 0ZM26 0C28.7614 0 31 2.23858 31 5L31 41C31 43.7614 28.7614 46 26 46C23.2386 46 21 43.7614 21 41L21 5C21 2.23858 23.2386 0 26 0Z"
            fill="#5E5E5E"
          />
        </svg>
      ) : (
        <svg
          width="35"
          height="47"
          viewBox="0 0 35 47"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M33.992 25.435C34.3029 25.2194 34.5571 24.9309 34.7327 24.5944C34.9083 24.2579 35 23.8834 35 23.5032C35 23.123 34.9083 22.7485 34.7327 22.412C34.5571 22.0754 34.3029 21.7869 33.992 21.5713L3.66075 0.419678C3.3109 0.174847 2.90114 0.0312738 2.47598 0.00455464C2.05081 -0.0221645 1.62651 0.0689923 1.24916 0.268124C0.871822 0.467255 0.555873 0.766742 0.335644 1.13405C0.115415 1.50135 -0.000670061 1.92243 9.40679e-07 2.35153L2.78982e-06 44.6548C0.00175831 45.0829 0.119337 45.5025 0.340093 45.8683C0.560849 46.2341 0.876431 46.5324 1.2529 46.7311C1.62937 46.9297 2.05248 47.0213 2.47674 46.9958C2.90099 46.9704 3.31034 46.8289 3.66075 46.5867L33.992 25.435Z"
            fill="#5E5E5E"
          />
        </svg>
      )}
    </div>
  );
};

export default ClusterResumePause;
