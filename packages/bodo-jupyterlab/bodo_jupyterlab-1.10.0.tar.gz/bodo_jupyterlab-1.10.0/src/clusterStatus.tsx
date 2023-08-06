import React from 'react';

type StatusProps = {
  status: string;
};

const ClusterStatus = ({ status }: StatusProps) => {
  return <div className={`cluster-status ${status.toLowerCase()}`}>{status}</div>;
};

export default ClusterStatus;
