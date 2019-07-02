import React from 'react';
import styled from '@emotion/styled';
import { H1, H2 } from '@blazingly-design/heading';

import Dropzone from '../components/dropzone';

export type DropzonePageProps = {
  onFileUpload: (file: FileList) => any;
};

const Wrapper = styled.div(() => {
  return {
    display: 'grid',
    gridGap: 50
  };
});

export default function DropzonePage(props: DropzonePageProps) {
  let { onFileUpload } = props;

  const handleSelectFile = (selectedFiles: FileList) => {
    if (!selectedFiles.length) return;

    onFileUpload(selectedFiles);
  };

  const handleDropzoneTrigger = () => {
    let inputElement = document.createElement('input');
    inputElement.type = 'file';
    inputElement.multiple = false;

    inputElement.addEventListener('change', function() {
      if (!this.files) return;
      // @ts-ignore...
      handleSelectFile([...this.files]);
    });
    inputElement.dispatchEvent(new MouseEvent('click'));
  };

  return (
    <Wrapper>
      <H1 color="white">Upload an audio file to get started...</H1>
      <Dropzone onTrigger={handleDropzoneTrigger} onDrop={handleSelectFile} />
    </Wrapper>
  );
}
