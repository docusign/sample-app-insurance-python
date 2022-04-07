import React, { useState, useEffect } from "react";
import { List } from "./List";
import { useTranslation } from "react-i18next";
import * as studentsAPI from "../../api/insuranceAPI";
import { download } from "../../api/download";
import { ApiDescription } from "./components/ApiDescription";

export const History = () => {
  const { t } = useTranslation("History");
  const [submissionsList, setSubmissionsList] = useState([]);

  useEffect(() => {
    async function getStatus() {
      try {
        let date = new Date();
        date.setUTCHours(0, 0, 0, 0);
        const fromDate = date.toISOString();
        const data = await studentsAPI.getStatus(fromDate);
        if (data.envelopes) {
          setSubmissionsList(data.envelopes);
        }
      } catch (error) {
        throw error;
      }
    }
    getStatus();
  }, []);

  async function onClick(event) {
    try {
      const data = await studentsAPI.getStatusDocument(
        event.envelopeId,
        event.documentId
      );

      download(
        data,
        `${event.envelopeId} - ${event.documentId}`,
        event.extention,
        event.mimeType
      );
    } catch (error) {
      throw error;
    }
  }

  if (submissionsList.length === 0) {
    return (
      <div className="text-center">
        <br></br>
        <h3>{t("EmptyListMessage")}</h3>
        <br></br>
      </div>
    );
  }
  return (
    <section className="container-fluid content-section">
      <h2 className="h2">{t("SubmissionsStatus")}</h2>
      <div class="row justify-content">
        <div class="col-lg-6">
          <div className="table-holder">
            <table className="table table-striped">
              <thead>
                <tr>
                  <th scope="col">{t("Subject")}</th>
                  <th scope="col">{t("Applicant")}</th>
                  <th scope="col">{t("Last Updated")}</th>
                </tr>
              </thead>
              <List list={submissionsList} onClick={onClick} />
            </table>
          </div>
        </div>
        <ApiDescription />
      </div>
    </section>
  );
};