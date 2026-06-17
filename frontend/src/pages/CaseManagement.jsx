import { useState } from "react";
import PageLayout from "../components/layout/PageLayout";
import { openCases, investigationNotes } from "../data/mockdata";
import { useTheme } from "../context/ThemeContext";

function PriorityBadge({ priority }) {
  const colors = {
    High: { bg: "#450a0a", color: "#f87171" },
    Medium: { bg: "#431407", color: "#fb923c" },
    Low: { bg: "#052e16", color: "#4ade80" },
  };
  const c = colors[priority] || colors.Low;
  return <span style={{ background: c.bg, color: c.color, padding: "4px 12px", borderRadius: "20px", fontSize: "12px", fontWeight: "600" }}>{priority}</span>;
}

function StatusBadge({ status }) {
  const colors = {
    Open: { bg: "#450a0a", color: "#f87171" },
    "In Progress": { bg: "#431407", color: "#fb923c" },
    Closed: { bg: "#052e16", color: "#4ade80" },
  };
  const c = colors[status] || colors.Open;
  return <span style={{ background: c.bg, color: c.color, padding: "4px 12px", borderRadius: "20px", fontSize: "12px", fontWeight: "600" }}>{status}</span>;
}

function CaseManagement() {
  const theme = useTheme();
  const [cases, setCases] = useState(openCases);
  const [selected, setSelected] = useState(null);
  const [notes, setNotes] = useState(investigationNotes);
  const [newNote, setNewNote] = useState("");
  const [filterStatus, setFilterStatus] = useState("All");

  const filtered = cases.filter((c) => filterStatus === "All" || c.status === filterStatus);

  const updateStatus = (id, newStatus) => {
    setCases((prev) => prev.map((c) => c.id === id ? { ...c, status: newStatus } : c));
    setSelected((prev) => prev ? { ...prev, status: newStatus } : prev);
  };

  const addNote = () => {
    if (!newNote.trim() || !selected) return;
    setNotes((prev) => [...prev, {
      id: prev.length + 1, case: selected.id,
      author: "Agent (You)", note: newNote.trim(),
      date: new Date().toISOString().split("T")[0],
    }]);
    setNewNote("");
  };

  const caseNotes = notes.filter((n) => n.case === selected?.id);

  const statCards = [
    { label: "Total Cases", value: cases.length, color: "#38bdf8" },
    { label: "Open", value: cases.filter(c => c.status === "Open").length, color: "#f87171" },
    { label: "In Progress", value: cases.filter(c => c.status === "In Progress").length, color: "#fb923c" },
    { label: "Closed", value: cases.filter(c => c.status === "Closed").length, color: "#4ade80" },
  ];

  return (
    <PageLayout title="Case Management">
      <div style={{ display: "flex", gap: "16px", marginBottom: "28px" }}>
        {statCards.map((card) => (
          <div key={card.label} style={{ flex: 1, background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "20px" }}>
            <div style={{ color: theme.subtext, fontSize: "13px", marginBottom: "8px" }}>{card.label}</div>
            <div style={{ color: card.color, fontSize: "28px", fontWeight: "700" }}>{card.value}</div>
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: "12px", marginBottom: "20px" }}>
        {["All", "Open", "In Progress", "Closed"].map((s) => (
          <button key={s} onClick={() => setFilterStatus(s)} style={{
            padding: "8px 18px", borderRadius: "8px", fontSize: "13px", cursor: "pointer",
            border: filterStatus === s ? "1px solid #38bdf8" : `1px solid ${theme.border}`,
            background: filterStatus === s ? "#1e3a5f" : theme.surface,
            color: filterStatus === s ? "#38bdf8" : theme.subtext,
          }}>{s}</button>
        ))}
      </div>

      <div style={{ display: "flex", gap: "20px" }}>
        <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: "12px" }}>
          {filtered.map((c) => (
            <div key={c.id} onClick={() => setSelected(c)} style={{
              background: theme.surface,
              border: selected?.id === c.id ? "1px solid #38bdf8" : `1px solid ${theme.border}`,
              borderRadius: "12px", padding: "18px", cursor: "pointer", transition: "all 0.2s",
            }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
                <span style={{ color: "#38bdf8", fontSize: "13px", fontWeight: "600" }}>{c.id}</span>
                <StatusBadge status={c.status} />
              </div>
              <div style={{ color: theme.text, fontSize: "15px", fontWeight: "500", marginBottom: "6px" }}>{c.title}</div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span style={{ color: theme.subtext, fontSize: "12px" }}>{c.account} · {c.date}</span>
                <PriorityBadge priority={c.priority} />
              </div>
            </div>
          ))}
        </div>

        <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: "16px" }}>
          <div style={{ background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "24px" }}>
            <h3 style={{ color: theme.text, fontSize: "15px", marginBottom: "16px" }}>Case Details</h3>
            {!selected ? (
              <p style={{ color: theme.subtext, fontSize: "14px" }}>Click a case to view details</p>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
                {[
                  { label: "Case ID", value: selected.id, color: "#38bdf8" },
                  { label: "Title", value: selected.title },
                  { label: "Account", value: selected.account },
                  { label: "Date Opened", value: selected.date },
                ].map(({ label, value, color }) => (
                  <div key={label} style={{ borderBottom: `1px solid ${theme.border}`, paddingBottom: "12px" }}>
                    <div style={{ color: theme.subtext, fontSize: "12px", marginBottom: "4px" }}>{label}</div>
                    <div style={{ color: color || theme.text, fontSize: "15px", fontWeight: "500" }}>{value}</div>
                  </div>
                ))}
                <div style={{ display: "flex", gap: "12px", borderBottom: `1px solid ${theme.border}`, paddingBottom: "12px" }}>
                  <div style={{ flex: 1 }}>
                    <div style={{ color: theme.subtext, fontSize: "12px", marginBottom: "6px" }}>Status</div>
                    <StatusBadge status={selected.status} />
                  </div>
                  <div style={{ flex: 1 }}>
                    <div style={{ color: theme.subtext, fontSize: "12px", marginBottom: "6px" }}>Priority</div>
                    <PriorityBadge priority={selected.priority} />
                  </div>
                </div>
                <div>
                  <div style={{ color: theme.subtext, fontSize: "12px", marginBottom: "10px" }}>Update Status</div>
                  <div style={{ display: "flex", gap: "8px" }}>
                    {["Open", "In Progress", "Closed"].map((s) => (
                      <button key={s} onClick={() => updateStatus(selected.id, s)} style={{
                        flex: 1, padding: "8px", borderRadius: "8px", fontSize: "12px", cursor: "pointer",
                        border: selected.status === s ? "1px solid #38bdf8" : `1px solid ${theme.border}`,
                        background: selected.status === s ? "#1e3a5f" : theme.bg,
                        color: selected.status === s ? "#38bdf8" : theme.subtext,
                      }}>{s}</button>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>

          <div style={{ background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "24px" }}>
            <h3 style={{ color: theme.text, fontSize: "15px", marginBottom: "16px" }}>Investigation Notes</h3>
            {!selected ? (
              <p style={{ color: theme.subtext, fontSize: "14px" }}>Select a case to view notes</p>
            ) : (
              <>
                <div style={{ display: "flex", flexDirection: "column", gap: "10px", marginBottom: "16px", maxHeight: "200px", overflowY: "auto" }}>
                  {caseNotes.length === 0 ? (
                    <p style={{ color: theme.subtext, fontSize: "13px" }}>No notes yet</p>
                  ) : caseNotes.map((n) => (
                    <div key={n.id} style={{ background: theme.bg, borderRadius: "8px", padding: "12px" }}>
                      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "6px" }}>
                        <span style={{ color: "#38bdf8", fontSize: "12px", fontWeight: "600" }}>{n.author}</span>
                        <span style={{ color: theme.subtext, fontSize: "11px" }}>{n.date}</span>
                      </div>
                      <div style={{ color: theme.text, fontSize: "13px" }}>{n.note}</div>
                    </div>
                  ))}
                </div>
                <div style={{ display: "flex", gap: "8px" }}>
                  <input
                    value={newNote}
                    onChange={(e) => setNewNote(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && addNote()}
                    placeholder="Add investigation note..."
                    style={{
                      flex: 1, background: theme.bg, border: `1px solid ${theme.border}`,
                      borderRadius: "8px", color: theme.text, padding: "10px 12px",
                      fontSize: "13px", outline: "none",
                    }}
                  />
                  <button onClick={addNote} style={{ padding: "10px 16px", borderRadius: "8px", background: "#2563eb", color: "white", border: "none", cursor: "pointer", fontSize: "13px", fontWeight: "600" }}>
                    Add
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </PageLayout>
  );
}

export default CaseManagement;