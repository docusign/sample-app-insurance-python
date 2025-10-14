import React from "react";
import PropTypes from "prop-types";
import { useTranslation } from "react-i18next";

export const ListItem = ({ item, onClick }) => {
  const { t } = useTranslation("History");
  const [open, setOpen] = React.useState(false);
  const ref = React.useRef(null);

  const toggle = () => setOpen(prev => !prev);
  const close = () => setOpen(false);

  React.useEffect(() => {
    function handleOutside(e) {
      if (ref.current && !ref.current.contains(e.target)) {
        close();
      }
    }
    function handleEsc(e) {
      if (e.key === "Escape") close();
    }

    document.addEventListener("mousedown", handleOutside);
    document.addEventListener("touchstart", handleOutside);
    document.addEventListener("keydown", handleEsc);
    return () => {
      document.removeEventListener("mousedown", handleOutside);
      document.removeEventListener("touchstart", handleOutside);
      document.removeEventListener("keydown", handleEsc);
    };
  }, []);

  const handleItemClick = (e, payload) => {
    e.preventDefault();
    // close first so UI updates immediately
    close();
    onClick(payload);
  };

  return (
    <tr>
      <td>{item.email_subject}</td>
      <td>{item.recipients?.signers?.[0]?.name}</td>
      <td>{new Date(item.status_changed_date_time).toDateString()}</td>
      <td className="text-right">
        <div className={`dropdown ${open ? "show" : ""}`} ref={ref}>
          <button
            type="button"
            className="btn btn-secondary dropdown-toggle"
            id={`options-${item.envelope_id}`}
            aria-haspopup="true"
            aria-expanded={open}
            onClick={toggle}
          >
            {t("OptionsButton")}
          </button>

          <div
            className={`dropdown-menu dropdown-menu-right ${open ? "show" : ""}`}
            aria-labelledby={`options-${item.envelope_id}`}
          >
            <a
              href="#/"
              className="dropdown-item"
              onClick={(e) =>
                handleItemClick(e, {
                  envelopeId: item.envelope_id,
                  documentId: "1",
                  extention: "pdf",
                  mimeType: "application/pdf"
                })
              }
            >
              {t("HTMLOptionButton")}
            </a>

            <a
              href="#/"
              className="dropdown-item"
              onClick={(e) =>
                handleItemClick(e, {
                  envelopeId: item.envelope_id,
                  documentId: "certificate",
                  extention: "pdf",
                  mimeType: "application/pdf"
                })
              }
            >
              {t("SummaryOptionButton")}
            </a>

            <a
              href="#/"
              className="dropdown-item"
              onClick={(e) =>
                handleItemClick(e, {
                  envelopeId: item.envelope_id,
                  documentId: "combined",
                  extention: "pdf",
                  mimeType: "application/pdf"
                })
              }
            >
              {t("CombinedOptionButton")}
            </a>
          </div>
        </div>
      </td>
    </tr>
  );
};

ListItem.propTypes = {
  item: PropTypes.object.isRequired,
  onClick: PropTypes.func.isRequired
};
