<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:gsm="http://www.sitemaps.org/schemas/sitemap/0.9">

<xsl:output method="html" version="1.0" encoding="utf-8" indent="yes"/>

<xsl:template match="/">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
  <meta name="generator" content="GNU make coupled with GNU awk to parse templates. Markdown to parse contents." />
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <meta name="author" content="Clément David" />
  <meta name="keywords" content="davidcl, clement, david, c.david86" />
  <meta name="description" content="Clément David's CV, articles and all official stuff." />
  <meta name="robots" content="all" />

  <title>Sitemap</title>
  
  <link rel="stylesheet" type="text/css" href="/davidcl/styles/light.css" media="all" />
  <link rel="stylesheet" type="text/css" href="/davidcl/styles/default.css" media="screen" />
  <link rel="Shortcut Icon" type="image/x-icon" href="/davidcl/favicon.ico" />
</head>

<body>
<div id="nonFooter">
    <div id="header"> <p><a href="/davidcl/index.xhtml">davidcl</a> > Sitemap</p> </div>
    <div id="toc"></div>
    <div id="contents">
      <ul>
      <xsl:for-each select="gsm:urlset/gsm:url">
        <li>
          <a>
            <xsl:attribute name="href"><xsl:value-of select="gsm:loc" /></xsl:attribute>
            <xsl:value-of select="gsm:loc" />
          </a>
        </li>
      </xsl:for-each>
      </ul>
    </div>
</div>
</body>
</html>
</xsl:template>

</xsl:stylesheet>

