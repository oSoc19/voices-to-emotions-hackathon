import React from 'react';
import styled from '@emotion/styled';

import SEO from '../components/seo';
import DropzonePage from '../components/dropzone-page';
import ResultPage from '../components/result-page';

export type FileUploadItem = {
  file: File;
  state: 'loading' | 'error' | 'success' | 'none';
};

const Main = styled.main(() => {
  return {
    padding: 20,
    margin: '0 auto',
    width: '100vw',
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'grey'
  };
});

const PageWrapper = styled.main(() => {
  return {
    backgroundColor: 'blue',
    borderRadius: 10,
    padding: 50,
    width: 960
  };
});

export default function IndexPage() {
  let [file, setFile] = React.useState<FileList | null>(null);

  return (
    <>
      <SEO title="Home" />
      <Main>
        <PageWrapper>{file ? <ResultPage file={file} /> : <DropzonePage onFileUpload={setFile} />}</PageWrapper>
      </Main>
    </>
  );
}
