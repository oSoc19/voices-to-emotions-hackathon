import React from 'react';
import styled from '@emotion/styled';

import Loader from '../components/loader';

export type DropzonePageProps = {
  file: FileList;
};

const Wrapper = styled.div(() => {
  return {
    display: 'grid',
    textAlign: 'center',
    paddingTop: 100
  };
});

const LoaderWrapper = styled.div(() => {
  return {
    display: 'grid',
    textAlign: 'center'
  };
});

export default function DropzonePage(props: DropzonePageProps) {
  return (
    <Wrapper>
      <Loader />
    </Wrapper>
  );
}
