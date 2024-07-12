<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="3.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
<xsl:output method="html" encoding="UTF-8" indent="yes"/>
<xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml"> 
        <section>
            <h2>RSS Feed</h2>
            <h2>
                <a hreflang="en" target="_blank">
                    <xsl:attribute name="href">
                        <xsl:value-of select="/rss/channel/atom:link/@href"/>
                    </xsl:attribute>
                    <xsl:value-of select="/rss/channel/title"/>
                </a>
            </h2>
            <p><xsl:value-of select="/rss/channel/description"/></p>
            <hr/>
            <xsl:for-each select="/rss/channel/item">
                <xsl:if test="not (position() > 5)">
                    <article>
                        <h3>
                            <a hreflang="en" target="_blank">
                                <xsl:attribute name="href">
                                    <xsl:value-of select="link"/>
                                </xsl:attribute>
                                <xsl:value-of select="title"/>
                            </a>
                        </h3>
                        <p><xsl:value-of select="description"/></p>
                        <footer>
                            <b>Publicado:</b>
                            <time>
                                <xsl:value-of select="pubDate"/>
                            </time>
                        </footer>
                    </article>
                </xsl:if>
            </xsl:for-each>
        </section>
    </html>
</xsl:template>
</xsl:stylesheet> 