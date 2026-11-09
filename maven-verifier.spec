Name:		maven-verifier
Version:	2.0.0
Release:	1
Summary:	Test harness that runs Maven
Group:		Development/Java
License:	Apache-2.0
URL:		https://maven.apache.org/shared/maven-verifier/
Source0:	https://github.com/apache/maven-verifier/archive/refs/tags/maven-verifier-%{version}.tar.gz#/maven-verifier-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python
# The maven RPM holds the class jars. maven-components owns the coordinates.
BuildRequires:	maven
BuildRequires:	maven-components >= 3.10.0
BuildRequires:	java-current-devel
BuildRequires:	mvn(org.apache.maven.shared:maven-shared-utils)
BuildRequires:	maven-shared-utils >= 3.5.0
Requires:	maven-shared-utils >= 3.5.0
BuildRequires:	mvn(org.apache.maven:maven-settings-builder)
BuildRequires:	mvn(org.apache.maven:maven-settings)
# settings-builder's POM depends on this. The Maven RPM only bundles a copy.
BuildRequires:	mvn(org.codehaus.plexus:plexus-sec-dispatcher)
BuildRequires:	plexus-sec-dispatcher
BuildRequires:	mvn(javax.inject:javax.inject)
# javax.inject and jakarta-inject both provide this coordinate.
BuildRequires:	javax.inject >= 1-2
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

Obsoletes:	maven-shared-verifier < %{EVRD}
Provides:	maven-shared-verifier = %{EVRD}
Obsoletes:	maven-verifier-javadoc < %{EVRD}
Obsoletes:	maven-shared-verifier-javadoc < %{EVRD}

%description
Forks or embeds Maven and checks the result of an integration test.
2.0.0 reads settings through maven-settings-builder and uses
maven-shared-utils 3.5. The sources do not use plexus-xml. Upstream
marks this component deprecated in favor of maven-executor. Tests are
not run.

%prep
%autosetup -n maven-verifier-maven-verifier-%{version}
rm -rf src/test .github
python - <<'PY'
import xml.etree.ElementTree as ET
NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def tag(name):
    return "{" + NS + "}" + name

def add(parent, name, text):
    node = ET.SubElement(parent, tag(name))
    node.text = text
    return node

root = ET.Element(tag("project"))
add(root, "modelVersion", "4.0.0")
add(root, "groupId", "org.apache.maven.shared")
add(root, "artifactId", "maven-verifier")
add(root, "version", "%{version}")
add(root, "name", "Apache Maven Verifier")
props = ET.SubElement(root, tag("properties"))
add(props, "maven.compiler.release", "8")
add(props, "project.build.sourceEncoding", "UTF-8")
deps = ET.SubElement(root, tag("dependencies"))
for group, artifact, version, scope in (
    ("org.apache.maven.shared", "maven-shared-utils", "3.5.0", ""),
    ("org.apache.maven", "maven-settings-builder", "3.10.0", "provided"),
    ("org.apache.maven", "maven-settings", "3.10.0", "provided"),
):
    dep = ET.SubElement(deps, tag("dependency"))
    add(dep, "groupId", group)
    add(dep, "artifactId", artifact)
    add(dep, "version", version)
    if scope:
        add(dep, "scope", scope)
ET.ElementTree(root).write("pom.xml", encoding="utf-8", xml_declaration=True)
PY

%files -f .mfiles
%doc LICENSE README.md MIGRATION.md
