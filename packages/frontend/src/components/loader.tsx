import * as React from 'react';
import { keyframes } from '@emotion/core';
import styled from '@emotion/styled';

const pulseAnimation = keyframes`
  0% {
    transform: scale3d(1, 1, 1);
  }

  50% {
    transform: scale3d(0.5, 0.5, 1);
  }

  100% {
    transform: scale3d(1, 1, 1);
  }
`;

const Circle = styled.div(() => {
  return {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    cursor: 'pointer',
    width: 400,
    height: 400,
    margin: '0 auto'
  };
});

const OuterCircle = styled.div(() => {
  return {
    position: 'absolute',
    width: 400,
    height: 400,
    borderRadius: 200,
    zIndex: 1001,
    backgroundColor: `rgba(255, 0, 0, 0.5)`,
    animation: `${pulseAnimation} 3s infinite`,
    animationTimingFunction: 'linear'
  };
});

const InnerCircle = styled.div(() => {
  return {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    width: 300,
    height: 300,
    borderRadius: 150,
    zIndex: 1002,
    backgroundColor: `rgba(255, 0, 0, 0.5)`,
    animation: `${pulseAnimation} 5s infinite`,
    animationTimingFunction: 'linear'
  };
});

export default function Loader() {
  return (
    <Circle>
      <InnerCircle />
      <OuterCircle />
    </Circle>
  );
}
