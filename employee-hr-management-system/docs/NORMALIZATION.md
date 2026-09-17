# Relational Normalization & Functional Dependency Analysis

This document provides the formal mathematical and relational proof that the **Employee & HR Management System** is strictly normalized up to **Third Normal Form (3NF)** without data redundancy or update anomalies.

---

## 1. Attribute Mapping & Notation

As defined in the project specification:

| Symbol | Attribute Name | Description |
|---|---|---|
| **$A$** | `Employee_ID` | Primary unique identifier for employees |
| **$B$** | `Department_ID` | Primary unique identifier for departments |
| **$C$** | `Department_Name` | Descriptive name of the department |
| **$D$** | `Manager_ID` | Unique identifier for department manager |
| **$E$** | `Manager_Name` | Full name of the department manager |
| **$F$** | `Project_ID` | Primary unique identifier for projects |
| **$G$** | `Project_Name` | Title of the enterprise project |
| **$H$** | `Project_Budget` | Financial budget allocated to the project |
| **$I$** | `Employee_Role` | Role assumed by an employee on a specific project |
| **$J$** | `Hours_Worked` | Total hours contributed by an employee to a project |

---

## 2. Functional Dependency Set ($F$)

The given set of functional dependencies governing the core enterprise domain is:

$$F = \{$$
1. **$A \to B$**: An employee belongs to exactly one department.
2. **$B \to C$**: A department ID uniquely determines its department name.
3. **$B \to D$**: A department ID uniquely determines its designated manager ID.
4. **$D \to E$**: A manager ID uniquely determines the manager's full name.
5. **$F \to G$**: A project ID uniquely determines the project's name.
6. **$F \to H$**: A project ID uniquely determines the project's allocated budget.
7. **$AF \to I$**: The combination of an employee and a project uniquely determines their specific role on that project.
8. **$AF \to J$**: The combination of an employee and a project uniquely determines the hours logged.
9. **$A \to D$**: An employee identifies their department manager (derived transitively from $A \to B$ and $B \to D$).
10. **$AF \to B$**: An employee assigned to a project determines their department (derived from $A \to B$ via augmentation).
$$\}$$

### Minimal Cover (Canonical Cover) Analysis
Notice that:
- $A \to D$ is redundant because $A \to B$ and $B \to D \implies A \to D$ by Armstrong's Transitivity Axiom.
- $AF \to B$ is redundant because $A \to B \implies AF \to B$ by Armstrong's Augmentation Axiom.

Thus, the irreducible canonical basis is:
$$F_c = \{ A \to B, B \to C, B \to D, D \to E, F \to G, F \to H, AF \to I, AF \to J \}$$

---

## 3. Step-by-Step Normalization Process

### 3.1 First Normal Form (1NF)
**Requirement**:
- Each attribute must contain only atomic (indivisible) values.
- There must be no repeating groups or multivalued arrays.
- A primary key must uniquely identify each tuple.

**Application to our System**:
- If an employee could be assigned to multiple projects within a single row (e.g., `Projects = [201, 202, 204]`), the relation would violate 1NF.
- **Resolution**: All many-to-many ($M:N$) relationships are extracted into dedicated bridge relations:
  1. `EMPLOYEE_PROJECT(Employee_ID, Project_ID, Assigned_Date, Employee_Role, Hours_Worked)`
  2. `EMPLOYEE_TRAINING(Employee_ID, Training_ID, Completion_Status, Score)`
- Every column in every table (`first_name`, `salary`, `date`, `check_in_time`, etc.) holds single atomic scalar values.
$$\implies \text{Database is strictly in 1NF.}$$

---

### 3.2 Second Normal Form (2NF)
**Requirement**:
- The relation must be in 1NF.
- There must be **no partial dependencies**: every non-prime attribute must depend on the **whole** candidate key, not on any proper subset of a composite candidate key.

**Application to our System**:
- The only tables possessing composite candidate keys are the bridge tables:
  - `EMPLOYEE_PROJECT` with composite key $\{ Employee\_ID, Project\_ID \}$ ($\{A, F\}$).
  - `EMPLOYEE_TRAINING` with composite key $\{ Employee\_ID, Training\_ID \}$.
- In `EMPLOYEE_PROJECT`:
  - Non-prime attributes are `Employee_Role` ($I$) and `Hours_Worked` ($J$).
  - Neither $A \to I$ nor $F \to I$ holds independently. An employee's role exists *only in the context of a project*, and a project has many roles filled by different employees. Thus, $AF \to I$ is a full functional dependency.
  - Similarly, hours worked ($J$) depends jointly on which employee worked on which project: $AF \to J$. Neither $A \to J$ nor $F \to J$ holds alone.
- If we had kept `Project_Name` ($G$) or `Project_Budget` ($H$) in `EMPLOYEE_PROJECT`, that would be a partial dependency ($F \to G, F \to H$ depends only on $F$, a proper subset of $\{A, F\}$).
- **Resolution**: `Project_Name` and `Budget` are separated into the independent `PROJECT` entity where $F$ is the complete primary key.
$$\implies \text{Database is strictly in 2NF.}$$

---

### 3.3 Third Normal Form (3NF)
**Requirement**:
- The relation must be in 2NF.
- There must be **no transitive dependencies**: for every non-trivial functional dependency $X \to Y$, either:
  1. $X$ is a superkey, OR
  2. $Y$ is a prime attribute (part of a candidate key).
- Informally: *"Every non-key attribute must depend on the key, the whole key, and nothing but the key (so help me Codd)."*

**Application to our System**:
- If `EMPLOYEE` contained:
  - `Department_Name` ($C$), then $A \to B$ and $B \to C$ would cause a transitive dependency $A \to C$ where $B$ is not a superkey of `EMPLOYEE`.
  - `Manager_Name` ($E$), then $A \to B \to D \to E$ would cause another transitive dependency.
- **Resolution**:
  - We decomposed the unnormalized schema into separate relations:
    1. `EMPLOYEE(Employee_ID [PK], ..., Department_ID [FK], HR_ID [FK])`
    2. `DEPARTMENT(Department_ID [PK], Department_Name, Location, Budget, Manager_Name)`
    3. `HR_MANAGER(HR_ID [PK], HR_Name, Email, Designation, Experience_Years)`
  - In `EMPLOYEE`, $Employee\_ID$ is the primary key and all non-key attributes (`salary`, `hire_date`, `email`, etc.) depend directly on $Employee\_ID$.
  - In `DEPARTMENT`, $Department\_ID$ is the primary key and determines $Department\_Name$, $Location$, $Budget$, and $Manager\_Name$.
$$\implies \text{Database is strictly in 3NF.}$$

---

## 4. Verification of Properties

1. **Lossless Join Decomposition**:
   - For every decomposition $R_1 \bowtie R_2 = R$, $R_1 \cap R_2 \to R_1$ or $R_1 \cap R_2 \to R_2$.
   - For example, `EMPLOYEE` $\cap$ `DEPARTMENT` = `Department_ID`, which is the primary key of `DEPARTMENT`. Therefore, joining `EMPLOYEE` and `DEPARTMENT` produces the exact original relation with no spurious tuples.

2. **Dependency Preservation**:
   - All original functional dependencies in $F$ ($A \to B$, $B \to C$, $B \to D$, $D \to E$, $F \to G$, $F \to H$, $AF \to I$, $AF \to J$) are enforced by the primary key and foreign key constraints across the normalized tables without requiring cross-table assertions.

---

## 5. Conclusion

The 12-table relational schema successfully achieves **3NF**, eliminating insert, update, and deletion anomalies while ensuring referential integrity through foreign key cascades and constraints.
